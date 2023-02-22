from flask import request
from ..modelos import Usuario, Tarea, UsuarioSchema, TareaSchema, db
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token
import os
import datetime

usuario_schema = UsuarioSchema()
tarea_schema = TareaSchema()

class VistaLogIn(Resource):
    def post(self):
        u_nombre = request.json["nombre"]
        u_contrasena = request.json["contrasena"]
        usuario = Usuario.query.filter_by(
            nombre=u_nombre, contrasena=u_contrasena).all()
        access_token= create_access_token(identity=request.json['name'])
        if usuario:
            return {'user':usuario_schema.dump(usuario),'access_token':access_token}
        else:
            return {'mensaje': 'Nombre de usuario o contraseña incorrectos'}, 401


class VistaSignIn(Resource):

    def post(self):
        if request.json["contrasena"] == request.json["contrasena_conf"]:
            nuevo_usuario = Usuario(
                nombre=request.json["nombre"],
                contrasena=request.json["contrasena"],
                email=request.json["email"]
            )
            access_token= create_access_token(identity=request.json['nombre'])
            db.session.add(nuevo_usuario)
            db.session.commit()
            return {'user':usuario_schema.dump(nuevo_usuario),'access_token':access_token}
        else:
            return {'mensaje':"La contraseña no es igual a la de confirmación."}

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena", usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204

class VistaTasks(Resource):
    @jwt_required()
    def post(self,id_user):
        file = request.files['file']
        _, extension = os.path.splitext(file.filename)
        file.save('uploads/' + file.filename)
        nueva_tarea= Tarea(
            nombre=request.json['nombre'],
            extension_original=extension,
            extension_convertir=request.json['extension_convertir'],
            fecha=datetime.datetime.now()
        )
        usuario = Usuario.query.get_or_404(id_user)
        usuario.tareas.append(nueva_tarea)
        return 'File uploaded successfully'
    @jwt_required()
    def get(self):
        return [tarea_schema.dump(tarea) for tarea in Tarea.query.all()]

class VistaTask(Resource):
    @jwt_required()
    def get(self,id_task):
        return tarea_schema.dump(Tarea.query.get_or_404(id_task))
    @jwt_required()    
    def delete(self,id_task):
        task = Tarea.query.get_or_404(id_task)
        db.session.delete(task)
        db.session.commit()
        return '',204
    
