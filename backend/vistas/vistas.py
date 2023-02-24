import os
from datetime import timedelta, datetime
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, asc
from flask_jwt_extended import jwt_required, create_access_token,get_jwt_identity
from ..modelos import Usuario, Tarea, UsuarioSchema, TareaSchema, db

usuario_schema = UsuarioSchema()
tarea_schema = TareaSchema()

'''
Login de un Usuario
'''
class VistaSignIn(Resource):
    def post(self):
        request.get_json(force=True)
        usuario = Usuario.query.get(request.json['email'])
        
        if usuario is None:
            return {'message':'El email ingresado no está registrado'}, 400
        
        if not usuario.verificar_clave(request.json['password']):
            return {'message': 'Contraseña incorrecta'}, 400
        
        try:
            access_token = create_access_token(identity = request.json['email'], expires_delta = timedelta(days = 1))
            return {
                'message':'Sesion iniciada',
                'access_token':access_token
            }
        
        except:
            return {'message':'Ha ocurrido un error'}, 500

'''
Registro de un usuario
'''
class VistaSignUp(Resource):

    def post(self):

        if Usuario.query.filter_by(email=request.json['email']).first() is not None:
            return {'message': f'El correo({request.json["email"]}) ya está registrado'}, 400
        
        if Usuario.query.filter_by(nombre=request.json['nombre']).first() is not None:
            return {'message': f'El nombre de usuario ({request.json["nombre"]}) ya está registrado'}, 400
        
        if request.json['email'] == '' or request.json['password'] == '' or request.json['password_confirmation'] == '' or request.json['nombre'] == '':
            return {'message': 'Campos invalidos'}, 400

        if request.json["password"] != request.json["password_confirmation"]:
            return {'mensaje':"La contraseña no es igual a la de confirmación."}
        
        nuevo_usuario = Usuario(
            nombre = request.json["nombre"],
            password = request.json["password"],
            email = request.json["email"]
        )

        nuevo_usuario.hashear_clave()
        
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            access_token = create_access_token(identity = request.json['email'], expires_delta = timedelta(days = 1))
            return {
                'message': f'El correo {request.json["email"]} ha sido registrado',
                'access_token': access_token 
            }

        except Exception as e:
            print(e)
            return {'message':'Ha ocurrido un error'}, 500            

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena", usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)
    
    def get(self):
        return [usuario_schema.dump(usuario) for usuario in Usuario.query.all()]

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204


'''
Obtener todas las tareas de un usuario y crear una tarea
'''
class VistaTasks(Resource):

    '''
    '''
    @jwt_required()
    def post(self):
        file = request.files['file']
        nombre_arch, extension = os.path.splitext(file.filename)
        file.save('uploads/' + file.filename)
        nueva_tarea= Tarea(
            nombre=request.form.get('nombre'),
            extension_original=extension,
            estado="uploaded",
            nombre_archivo=nombre_arch,
            extension_convertir=request.form.get('extension_convertir'),
            fecha=datetime.now(),
            usuarios=get_jwt_identity()
        )
        db.session.add(nueva_tarea)
        db.session.commit()
        usuario = Usuario.query.get_or_404(get_jwt_identity())
        usuario.tareas.append(nueva_tarea)
        return {"tarea":tarea_schema.dump(nueva_tarea)}
    
    '''
    Recuperar todas las tareas de conversión de un usuario autorizado.
    '''
    @jwt_required()
    def get(self):
        max_tasks = request.args.get('max_tasks')
        order = request.args.get('order')
        print("Hola bom shía" + get_jwt_identity())
        if int(order):
            return [tarea_schema.dump(tarea) for tarea in Tarea.query.filter(Tarea.usuarios==get_jwt_identity()).order_by(desc(Tarea.id)).limit(max_tasks).all()]
        else:
            return [tarea_schema.dump(tarea) for tarea in Tarea.query.filter(Tarea.usuarios==get_jwt_identity()).order_by(asc(Tarea.id)).limit(max_tasks).all()]

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
    
# class VistaFile(Resource):
#     @jwt_required()
#     def get(self,id_task):
#         return tarea_schema.dump(Tarea.query.get_or_404(id_task))
