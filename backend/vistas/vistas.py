from flask import request
from ..modelos import db, Usuario, UsuarioSchema, TareaSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token

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
        nuevo_usuario = Usuario(
            nombre=request.json["nombre"],
            contrasena=request.json["contrasena"],
            email=request.json["email"]
        )
        access_token= create_access_token(identity=request.json['nombre'])
        db.session.add(nuevo_usuario)
        db.session.commit()
        return {'user':usuario_schema.dump(nuevo_usuario),'access_token':access_token}

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

class VistaUploadTask(Resource):
    def post(self):
        file = request.files['file']
        file.save('uploads/' + file.filename)
        return 'File uploaded successfully'