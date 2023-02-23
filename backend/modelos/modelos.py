from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

import enum

# testcommit
db = SQLAlchemy()

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    extension_original = db.Column(db.String(20))
    extension_convertir = db.Column(db.String(20))
    estado = db.Column(db.String(50), nullable = False)
    fecha = db.Column(db.DateTime(), default = datetime.now())
    user = db.Column(db.String(80) ,db.ForeignKey('usuario.email'))

class Usuario(db.Model):
    nombre = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(150))
    email = db.Column(db.String(80), primary_key = True)
    tareas = db.relationship('Tarea', cascade='all, delete, delete-orphan')

    def hashear_clave(self):
        '''
        Hashea la clave en la base de datos
        '''
        self.password = generate_password_hash(self.password, 'sha256')

    def verificar_clave(self, clave):
        '''
        Verifica la clave hasheada con la del parámetro
        '''
        return check_password_hash(self.password, clave)

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Usuario
         include_relationships = True
         load_instance = True

class TareaSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Tarea
         include_relationships = True
         load_instance = True
