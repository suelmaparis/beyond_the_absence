import pandas as pd
#import seaborn as sns
import os
import smtplib
import random
from flask import Flask, render_template, request, flash, redirect, url_for
from email.mime.text import MIMEText

from dotenv import load_dotenv
load_dotenv()

MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

app = Flask(__name__)


app.secret_key = 'um_valor_secreto_aqui'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

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

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
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
    from country_continent_map import country_continent_map
   
    # ===== 1. CARREGAR DADOS MUNDIAIS =====
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

    # ===== 2. CARREGAR DADOS DAS MÃES =====
    df_moms = pd.read_csv('db/single_mom_dataset.csv')

    def random_color():
        return f"rgba({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)}, 0.5)"
    def generate_colors(n):
        bg = [random_color() for _ in range(n)]
        border = [color.replace('0.5', '1') for color in bg]
        return bg, border

    # AGE
    if 'age' in df_moms.columns:
        df_moms = df_moms.dropna(subset=['age'])
        df_moms['age'] = df_moms['age'].astype(int)
        age_counts = df_moms['age'].value_counts().sort_index()
        age_labels = age_counts.index.tolist()
        age_data = age_counts.values.tolist()
        age_colors, age_borders = generate_colors(len(age_labels))
    else:
        age_labels, age_data, age_colors, age_borders = [], [], [], []

    # FEELING ANXIOUS
    anxious_counts = df_moms['Feeling anxious'].value_counts()
    anxious_labels = anxious_counts.index.tolist()
    anxious_data = anxious_counts.values.tolist()
    anxious_colors, anxious_borders = generate_colors(len(anxious_labels))

    # SUICIDE ATTEMPT
    suicide_counts = df_moms['Suicide attempt'].value_counts()
    suicide_labels = suicide_counts.index.tolist()
    suicide_data = suicide_counts.values.tolist()
    suicide_colors, _ = generate_colors(len(suicide_labels))

    # TROUBLE SLEEPING
    sleep_counts = df_moms['Trouble sleeping at night'].value_counts()
    sleep_labels = sleep_counts.index.tolist()
    sleep_data = sleep_counts.values.tolist()
    sleep_colors, sleep_borders = generate_colors(len(sleep_labels))

    # PROBLEMS OF BONDING
    bonding_counts = df_moms['Problems of bonding with baby'].value_counts()
    bonding_labels = bonding_counts.index.tolist()
    bonding_data = bonding_counts.values.tolist()
    bonding_colors, bonding_borders = generate_colors(len(bonding_labels))

    #Top 10 países com maior % de mulheres (2022)
    top10_df = df_world[['Country Name', '2022']].dropna().sort_values(by='2022', ascending=False).head(10)
    top10_labels = top10_df['Country Name'].tolist()
    top10_data = top10_df['2022'].tolist()
    top10_colors, top10_borders = generate_colors(len(top10_labels))
   
    #Comparação entre 2010 e 2022 por continente (Bar 
    if '2010' in df_world.columns:
        comparison_df = df_world.dropna(subset=['2010', '2022'])
        comp_group = comparison_df.groupby('Continent')[['2010', '2022']].mean().round(2)
        comp_labels = comp_group.index.tolist()
        data_2010 = comp_group['2010'].tolist()
        data_2022 = comp_group['2022'].tolist()
        comp_colors, _ = generate_colors(len(comp_labels))

    continent_colors, continent_borders = generate_colors(len(continent_labels))
 


    # ===== 3. ENVIAR PARA TEMPLATE =====
    return render_template('index.html',
    age_labels=age_labels, age_data=age_data,
    age_colors=age_colors, age_borders=age_borders,

    anxious_labels=anxious_labels, anxious_data=anxious_data,
    anxious_colors=anxious_colors, anxious_borders=anxious_borders,

    suicide_labels=suicide_labels, suicide_data=suicide_data,
    suicide_colors=suicide_colors,

    sleep_labels=sleep_labels, sleep_data=sleep_data,
    sleep_colors=sleep_colors, sleep_borders=sleep_borders,

    bonding_labels=bonding_labels,
    bonding_data=bonding_data,
    bonding_colors=bonding_colors,
    bonding_borders=bonding_borders,

    continent_labels=continent_labels,
    continent_values=continent_values,
    continent_colors=continent_colors,
    continent_borders=continent_borders,

    top10_labels=top10_labels,
    top10_data=top10_data,
    top10_colors=top10_colors,
    top10_borders=top10_borders,

    comp_labels=comp_labels,
    data_2010=data_2010,
    data_2022=data_2022,
    comp_colors=comp_colors,

)