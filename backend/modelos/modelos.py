from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

# testcommit
db = SQLAlchemy()



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True)
    contrasena = db.Column(db.String(50))
    email = db.Column(db.String(80), unique=True)
    tareas = db.relationship('Task',backref = 'user', lazy = True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    extension_original = db.Column(db.String(20))
    extension_convertir = db.Column(db.String(20))
    estado=db.Column(db.String(50),nullable=False)
    fecha= db.Column(db.DateTime)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

class TareaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
