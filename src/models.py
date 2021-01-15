from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

#creando la tabla de la base de datos
class Post(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    text_post = db.Column(db.String(250),nullable=False)
    date_post = db.Column(db.DateTime, default=datetime.datetime.utcnow)

#constructor para iniciar los valores
    def __init__(self, text):
        self.text_post = text

#funcion que retorna los datos 
    def serialize(self):
        return{
            "id": self.id,
            "text_post": self.text_post,
            "date_post ": self.date_post
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
