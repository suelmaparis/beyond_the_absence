import pandas as pd
import os
import smtplib
import random
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from email.mime.text import MIMEText
from flask_login import login_user, logout_user, login_required
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.security import check_password_hash

from flask_migrate import Migrate


from models import db, BlogPost, Comment, User, Resource, Question, Tip, CheckIn, Event
from flask_login import LoginManager

from dotenv import load_dotenv
load_dotenv()


MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

app = Flask(__name__)

migrate = Migrate(app, db)

db_url = os.environ.get("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  

class AuthModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return super().index()

admin = Admin(app, name='Beyond Admin', template_mode='bootstrap4', index_view=MyAdminIndexView())
admin.add_view(AuthModelView(Resource, db.session))
admin.add_view(AuthModelView(BlogPost, db.session))
admin.add_view(AuthModelView(Question, db.session))
admin.add_view(AuthModelView(Tip, db.session))
admin.add_view(AuthModelView(Event, db.session))

def get_dashboard_data():
    from country_continent_map import country_continent_map
    import random
    import pandas as pd

    # ===== Carregar os dados principais =====
    df_world = pd.read_csv('db/mom_world_dataset.csv', skiprows=4)
    df_special = pd.read_excel("db/special_needs_moms.xlsx", header=0)
    df_special.columns = df_special.columns.str.strip().str.lower().str.replace(' ', '_')

    # Renomear colunas para facilitar leitura
    df_special.rename(columns={
        'category': 'population_group',
        'total': 'value_total',
        'children_with_functional_difficulties': 'value_with_difficulty',
        'children_without_functional_difficulties': 'value_without_difficulty',
        'countries_and_areas': 'country',
        'development_regions': 'development_status'
    }, inplace=True)

    # Garantir que os dados são numéricos
    df_special['value_total'] = pd.to_numeric(df_special['value_total'], errors='coerce')
    df_special['value_with_difficulty'] = pd.to_numeric(df_special['value_with_difficulty'], errors='coerce')
    df_special['value_without_difficulty'] = pd.to_numeric(df_special['value_without_difficulty'], errors='coerce')

    df_moms = pd.read_csv('db/single_mom_dataset.csv')

    # ===== Fun��es auxiliares para cores =====
    def random_color():
        return f"rgba({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)}, 0.5)"
    def generate_colors(n):
        bg = [random_color() for _ in range(n)]
        border = [color.replace('0.5', '1') for color in bg]
        return bg, border

    # ===== Vari�veis de gr�ficos =====
    age_labels, age_data, age_colors, age_borders = [], [], [], []
    anxious_labels, anxious_data, anxious_colors, anxious_borders = [], [], [], []
    suicide_labels, suicide_data, suicide_colors = [], [], []
    sleep_labels, sleep_data, sleep_colors, sleep_borders = [], [], [], []
    bonding_labels, bonding_data, bonding_colors, bonding_borders = [], [], [], []

    continent_labels, continent_values, continent_colors, continent_borders = [], [], [], []
    top10_labels, top10_data, top10_colors, top10_borders = [], [], [], []
    comp_labels, data_2010, data_2022, comp_colors = [], [], [], []

    special_labels, special_values, special_colors, special_borders = [], [], [], []
    lowest_labels, lowest_values, lowest_colors, lowest_borders = [], [], [], []
    dev_labels, dev_values = [], []

    # ===== AGE =====
    if 'age' in df_moms.columns:
        df_moms = df_moms.dropna(subset=['age'])
        df_moms['age'] = df_moms['age'].astype(int)
        age_counts = df_moms['age'].value_counts().sort_index()
        age_labels = age_counts.index.tolist()
        age_data = age_counts.values.tolist()
        age_colors, age_borders = generate_colors(len(age_labels))

    # ===== MENTAL HEALTH INDICATORS =====
    anxious_counts = df_moms['Feeling anxious'].value_counts()
    anxious_labels = anxious_counts.index.tolist()
    anxious_data = anxious_counts.values.tolist()
    anxious_colors, anxious_borders = generate_colors(len(anxious_labels))

    suicide_counts = df_moms['Suicide attempt'].value_counts()
    suicide_labels = suicide_counts.index.tolist()
    suicide_data = suicide_counts.values.tolist()
    suicide_colors, _ = generate_colors(len(suicide_labels))

    sleep_counts = df_moms['Trouble sleeping at night'].value_counts()
    sleep_labels = sleep_counts.index.tolist()
    sleep_data = sleep_counts.values.tolist()
    sleep_colors, sleep_borders = generate_colors(len(sleep_labels))

    bonding_counts = df_moms['Problems of bonding with baby'].value_counts()
    bonding_labels = bonding_counts.index.tolist()
    bonding_data = bonding_counts.values.tolist()
    bonding_colors, bonding_borders = generate_colors(len(bonding_labels))

    # ===== CONTINENT VIEW =====
    excluidos = [
        'Africa Eastern and Southern', 'Africa Western and Central', 'Arab World',
        'World', 'High income', 'Low income', 'Upper middle income',
        'Lower middle income', 'Low & middle income', 'OECD members',
        'Fragile and conflict affected situations', 'Latin America & Caribbean',
        'Sub-Saharan Africa', 'Europe & Central Asia', 'Middle East & North Africa',
        'South Asia', 'East Asia & Pacific'
    ]
    df_world = df_world[~df_world['Country Name'].isin(excluidos)]
    df_world['Continent'] = df_world['Country Name'].map(country_continent_map)
    df_world = df_world.dropna(subset=['Continent', '2022'])

    continent_group = df_world.groupby('Continent')['2022'].mean().round(2)
    continent_labels = continent_group.index.tolist()
    continent_values = continent_group.values.tolist()
    continent_colors, continent_borders = generate_colors(len(continent_labels))

    # ===== TOP 10 COUNTRIES =====
    top10_df = df_world[['Country Name', '2022']].dropna().sort_values(by='2022', ascending=False).head(10)
    top10_labels = top10_df['Country Name'].tolist()
    top10_data = top10_df['2022'].tolist()
    top10_colors, top10_borders = generate_colors(len(top10_labels))

    # ===== COMPARISON 2010 vs 2022 =====
    if '2010' in df_world.columns:
        comparison_df = df_world.dropna(subset=['2010', '2022'])
        comp_group = comparison_df.groupby('Continent')[['2010', '2022']].mean().round(2)
        comp_labels = comp_group.index.tolist()
        data_2010 = comp_group['2010'].tolist()
        data_2022 = comp_group['2022'].tolist()
        comp_colors, _ = generate_colors(len(comp_labels))

    # ===== SPECIAL NEEDS: Group Summary (Gender/Urban/Rural) =====
    special_group_summary = df_special[
        (df_special['indicator'] == 'ANAR Primary') &
        (df_special['population_group'].isin(['Male', 'Female']))
    ]
    if not special_group_summary.empty:
        grouped = special_group_summary.groupby('population_group')['value_total'].mean().round(2)
        special_labels = grouped.index.tolist()
        special_values = grouped.values.tolist()
        special_colors, special_borders = generate_colors(len(special_labels))

    # ===== SPECIAL NEEDS: Lowest 10 countries =====
    lowest_df = df_special[
        (df_special['indicator'] == 'ANAR Primary') &
        (df_special['population_group'] == 'Total')
    ].dropna(subset=['value_with_difficulty'])

    if not lowest_df.empty:
        lowest_sorted = lowest_df.sort_values(by='value_with_difficulty').head(10)
        lowest_labels = lowest_sorted['country'].tolist()
        lowest_values = lowest_sorted['value_with_difficulty'].tolist()
        lowest_colors, lowest_borders = generate_colors(len(lowest_labels))

    # ===== SPECIAL NEEDS: By Development Status =====
    dev_df = df_special[
        (df_special['indicator'] == 'ANAR Primary') &
        (df_special['population_group'] == 'Total')
    ]
    if not dev_df.empty:
        grouped_dev = dev_df.groupby('development_status')['value_with_difficulty'].mean().round(2)
        dev_labels = grouped_dev.index.tolist()
        dev_values = grouped_dev.values.tolist()

    # ===== SPECIAL NEEDS: Urban vs Rural Average =====
    avg_urban = None
    avg_rural = None

    urban_data = df_special[
        (df_special['indicator'] == 'ANAR Primary') &
        (df_special['population_group'] == 'Urban')
    ]
    rural_data = df_special[
        (df_special['indicator'] == 'ANAR Primary') &
        (df_special['population_group'] == 'Rural')
    ]

    if not urban_data.empty:
        avg_urban = round(urban_data['value_with_difficulty'].mean(), 2)
    if not rural_data.empty:
        avg_rural = round(rural_data['value_with_difficulty'].mean(), 2)

    # ===== Return para o template =====
    return dict(
        age_labels=age_labels, age_data=age_data, age_colors=age_colors, age_borders=age_borders,
        anxious_labels=anxious_labels, anxious_data=anxious_data, anxious_colors=anxious_colors, anxious_borders=anxious_borders,
        suicide_labels=suicide_labels, suicide_data=suicide_data, suicide_colors=suicide_colors,
        sleep_labels=sleep_labels, sleep_data=sleep_data, sleep_colors=sleep_colors, sleep_borders=sleep_borders,
        bonding_labels=bonding_labels, bonding_data=bonding_data, bonding_colors=bonding_colors, bonding_borders=bonding_borders,
        continent_labels=continent_labels, continent_values=continent_values, continent_colors=continent_colors, continent_borders=continent_borders,
        top10_labels=top10_labels, top10_data=top10_data, top10_colors=top10_colors, top10_borders=top10_borders,
        comp_labels=comp_labels, data_2010=data_2010, data_2022=data_2022, comp_colors=comp_colors,
        special_labels=special_labels, special_values=special_values, special_colors=special_colors, special_borders=special_borders,
        lowest_labels=lowest_labels, lowest_values=lowest_values, lowest_colors=lowest_colors, lowest_borders=lowest_borders,
        dev_labels=dev_labels, dev_values=dev_values, avg_urban=avg_urban, avg_rural=avg_rural
    )



@app.route('/send_email', methods=['POST'])
def send_email():
    Name = request.form.get('Name', '')
    Phone = request.form.get('Phone', '')
    Email = request.form.get('Email', '')
    Message = request.form.get('Message', '')

    if not (Name and Phone and Email and Message):
        flash('All fields are required.')
        return redirect(url_for('index'))

    try:
        msg = MIMEText(f"New message from {Name} ({Phone}) <{Email}>:\n\n{Message}")
        msg['Subject'] = 'New Message from a Mom'
        msg['From'] = MAIL_USERNAME
        msg['To'] = MAIL_USERNAME  # send to yourself

        with smtplib.SMTP('mail.privateemail.com', 587) as server:
            server.starttls()
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.send_message(msg)

        flash('Email sent successfully!')
    except Exception as e:
        print("Email sending error:", e)
        flash('Error sending email. Please try again.')

    return redirect(url_for('index'))

@app.route('/')
def index():
    dashboard_data = get_dashboard_data()

    resources = Resource.query.all()
    category_labels = {
        'Health': '🏥 Health Services and Prenatal Care',
        'Mental': '🤱 Support Groups & Mental Health',
        'Housing': '🏠 Housing Assistance & Shelters',
        'Resources': '🍎 Material & Logistic & Food Support',
        'Jobs': '💼 Employment & Job Readiness',
        'Legal': '⚖️ Legal Aid Services'
    }

    return render_template('index.html', 
        resources=resources,
        category_labels=category_labels,
        **dashboard_data
    )

@app.route('/checkin', methods=['POST'])
def checkin():
    from sqlalchemy.sql import func

    data = request.get_json()
    mood = data.get("mood")
    user_agent = request.headers.get('User-Agent', 'anonymous')

    tips = []
    suggested_resources = []

    if mood:
        checkin = CheckIn(mood=mood, user_agent=user_agent)
        db.session.add(checkin)
        db.session.commit()

        tips_objs = Tip.query.filter_by(category=mood).order_by(func.random()).limit(3).all()
        tips = [tip.message for tip in tips_objs]

        category_map = {
            "anxious": "Mental",
            "depressed": "Mental",
            "no_food": "Resources",
            "tired": "Health",
            "low_self_esteem": "Health"
        }
        category = category_map.get(mood)
        if category:
            resources = Resource.query.filter_by(category=category).limit(4).all()
            suggested_resources = [{
                "title": r.title,
                "description": r.description,
                "address": r.address,
                "phone": r.phone,
                "website": r.website,
                "category": r.category
            } for r in resources]

    return jsonify({"tips": tips, "resources": suggested_resources})

@app.route('/blog')
def blog():
    posts = BlogPost.query.order_by(BlogPost.date.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    post = BlogPost.query.get_or_404(post_id)
    post.likes += 1
    db.session.commit()
    return redirect(url_for('blog'))

@app.route('/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    name = request.form['name']
    text = request.form['text']
    new_comment = Comment(post_id=post_id, name=name, text=text)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('blog'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect('/admin')
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/api/questions')
def get_questions():
    questions = Question.query.all()
    return jsonify([{'id': q.id, 'text': q.text, 'category': q.category} for q in questions])

@app.route('/api/events')
def get_events():
    events = Event.query.all()
    return jsonify([{
        'name': e.name,
        'date': e.date,
        'time': e.time,
        'location': e.location,
        'description': e.description,
        'link': e.link
    } for e in events])

