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


from models import db, BlogPost, Comment, User, Resource, Question, Tip, CheckIn
from flask_login import LoginManager

from dotenv import load_dotenv
load_dotenv()


MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

app = Flask(__name__)

migrate = Migrate(app, db)

app.secret_key = 'um_valor_secreto_aqui'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
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

def get_dashboard_data():
    from country_continent_map import country_continent_map

    df_world = pd.read_csv('db/mom_world_dataset.csv', skiprows=4)

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

    df_moms = pd.read_csv('db/single_mom_dataset.csv')

    def random_color():
        return f"rgba({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)}, 0.5)"
    def generate_colors(n):
        bg = [random_color() for _ in range(n)]
        border = [color.replace('0.5', '1') for color in bg]
        return bg, border

    age_labels, age_data, age_colors, age_borders = [], [], [], []
    if 'age' in df_moms.columns:
        df_moms = df_moms.dropna(subset=['age'])
        df_moms['age'] = df_moms['age'].astype(int)
        age_counts = df_moms['age'].value_counts().sort_index()
        age_labels = age_counts.index.tolist()
        age_data = age_counts.values.tolist()
        age_colors, age_borders = generate_colors(len(age_labels))

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

    top10_df = df_world[['Country Name', '2022']].dropna().sort_values(by='2022', ascending=False).head(10)
    top10_labels = top10_df['Country Name'].tolist()
    top10_data = top10_df['2022'].tolist()
    top10_colors, top10_borders = generate_colors(len(top10_labels))

    if '2010' in df_world.columns:
        comparison_df = df_world.dropna(subset=['2010', '2022'])
        comp_group = comparison_df.groupby('Continent')[['2010', '2022']].mean().round(2)
        comp_labels = comp_group.index.tolist()
        data_2010 = comp_group['2010'].tolist()
        data_2022 = comp_group['2022'].tolist()
        comp_colors, _ = generate_colors(len(comp_labels))
    else:
        comp_labels, data_2010, data_2022, comp_colors = [], [], [], []

    continent_colors, continent_borders = generate_colors(len(continent_labels))

    return dict(
        age_labels=age_labels, age_data=age_data, age_colors=age_colors, age_borders=age_borders,
        anxious_labels=anxious_labels, anxious_data=anxious_data, anxious_colors=anxious_colors, anxious_borders=anxious_borders,
        suicide_labels=suicide_labels, suicide_data=suicide_data, suicide_colors=suicide_colors,
        sleep_labels=sleep_labels, sleep_data=sleep_data, sleep_colors=sleep_colors, sleep_borders=sleep_borders,
        bonding_labels=bonding_labels, bonding_data=bonding_data, bonding_colors=bonding_colors, bonding_borders=bonding_borders,
        continent_labels=continent_labels, continent_values=continent_values, continent_colors=continent_colors, continent_borders=continent_borders,
        top10_labels=top10_labels, top10_data=top10_data, top10_colors=top10_colors, top10_borders=top10_borders,
        comp_labels=comp_labels, data_2010=data_2010, data_2022=data_2022, comp_colors=comp_colors
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
    data = request.get_json()

    mood = data.get('mood')
    tips = []
    resources = []

    # Exemplo simples — personalize conforme suas regras
    if mood == 'tired':
        tips.append("Try to rest for 10 minutes if possible.")
        resources.append({
            "title": "Free Nap Rooms",
            "description": "Quiet spaces for moms to rest.",
            "address": "456 Peaceful Lane",
            "phone": "555-REST",
            "website": "https://nap.example.com"
        })

    if mood == 'no_food':
        tips.append("Don't be afraid to ask for help — you're not alone.")
        resources.append({
            "title": "Emergency Food Program",
            "description": "Get free groceries and baby food.",
            "address": "789 Community Dr",
            "phone": "555-FOOD",
            "website": "https://foodhelp.example.com"
        })

    return jsonify({
        "tips": tips,
        "resources": resources
    })

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

