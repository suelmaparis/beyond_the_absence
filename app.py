import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        Name = request.form.get('Name', '')
        Phone = request.form.get('Phone', '')
        Email = request.form.get('Email', '')
        Message = request.form.get('Message', '')

        if not (Name and Phone and Email and Message):
            flash('All fields are required.')
            return redirect(url_for('index'))

        try:
            msg = MIMEText(f"New message from {Name} {Phone} <{Email}>:\n\n{Message}")
            msg['Subject'] = 'New Message from a Mom'
            msg['From'] = 'seuemail@dominio.com'
            msg['To'] = 'suelmaparis@hotmail.com'

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('suelmaparis@hotmail.com', 'Vannessa-1234')
                server.send_message(msg)

            flash('Email sent successfully!')
        except Exception as e:
            print(e)
            flash('Error sending email.')

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    
@app.route('/')
def index():
    df = pd.read_csv('db/single_mom_dataset.csv')

    def random_color():
        return f"rgba({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)}, 0.5)"

    def generate_colors(n):
        bg = [random_color() for _ in range(n)]
        border = [color.replace('0.5', '1') for color in bg]
        return bg, border

    # AGE
    if 'age' in df.columns:
        df = df.dropna(subset=['age'])
        df['age'] = df['age'].astype(int)
        age_counts = df['age'].value_counts().sort_index()
        age_labels = age_counts.index.tolist()
        age_data = age_counts.values.tolist()
        age_colors, age_borders = generate_colors(len(age_labels))
    else:
        age_labels, age_data, age_colors, age_borders = [], [], [], []

    # FEELING ANXIOUS
    anxious_counts = df['Feeling anxious'].value_counts()
    anxious_labels = anxious_counts.index.tolist()
    anxious_data = anxious_counts.values.tolist()
    anxious_colors, anxious_borders = generate_colors(len(anxious_labels))

    # SUICIDE ATTEMPT
    suicide_counts = df['Suicide attempt'].value_counts()
    suicide_labels = suicide_counts.index.tolist()
    suicide_data = suicide_counts.values.tolist()
    suicide_colors, _ = generate_colors(len(suicide_labels))  # border optional

    # TROUBLE SLEEPING
    sleep_counts = df['Trouble sleeping at night'].value_counts()
    sleep_labels = sleep_counts.index.tolist()
    sleep_data = sleep_counts.values.tolist()
    sleep_colors, sleep_borders = generate_colors(len(sleep_labels))

    return render_template(
        'index.html',
        age_labels=age_labels,
        age_data=age_data,
        age_colors=age_colors,
        age_borders=age_borders,
        anxious_labels=anxious_labels,
        anxious_data=anxious_data,
        anxious_colors=anxious_colors,
        anxious_borders=anxious_borders,
        suicide_labels=suicide_labels,
        suicide_data=suicide_data,
        suicide_colors=suicide_colors,
        sleep_labels=sleep_labels,
        sleep_data=sleep_data,
        sleep_colors=sleep_colors,
        sleep_borders=sleep_borders
    )

