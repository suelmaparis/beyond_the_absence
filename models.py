from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'))
    name = db.Column(db.String(100))
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(300))
    title = db.Column(db.String(500))
    description = db.Column(db.Text)
    email = db.Column(db.String(300))
    website = db.Column(db.String(500))
    phone = db.Column(db.String(200))
    address = db.Column(db.String(500))
    tags = db.Column(db.String(300))


class CheckIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Sentimento principal selecionado
    mood = db.Column(db.String(100), nullable=False)

    # Respostas de perguntas adicionais (sim/não)
    anxious = db.Column(db.Boolean)
    depressed = db.Column(db.Boolean)
    no_food = db.Column(db.Boolean)
    body_discomfort = db.Column(db.Boolean)

    # Hábitos saudáveis (extras)
    exercised = db.Column(db.Boolean)
    drank_water = db.Column(db.Boolean)
    skincare = db.Column(db.Boolean)
    went_outside = db.Column(db.Boolean)
    made_bed = db.Column(db.Boolean)

    # Metadados
    user_agent = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Tip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))  
    message = db.Column(db.Text)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False) 

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    date = db.Column(db.String(50))        
    time = db.Column(db.String(50))
    location = db.Column(db.String(200))
    description = db.Column(db.Text)
    link = db.Column(db.String(300))
    frequency = db.Column(db.String(50)) 

