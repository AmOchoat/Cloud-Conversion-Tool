from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

# testcommit
db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    email = db.Column(db.String(80), unique=True)
    tareas = db.relationship('Tarea', cascade='all, delete, delete-orphan')


class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}

class Tarea(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    extencion_original = db.Column(db.String(20))
    extencion_convertir = db.Column(db.String(20))
    estado=db.Column(db.String(50),nullable=False)
    init_date= db.Column(db.DateTime)
    usuario=db.Column(db.Integer,db.ForeignKey('usuario.id'))

class TareaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model=Tarea
        include_relationships = True
        load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True
