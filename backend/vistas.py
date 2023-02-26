
import os
from datetime import timedelta, datetime
from flask import request
from flask_cors import cross_origin
from flask_restful import Resource
from sqlalchemy import desc, asc , or_ , and_
from flask_jwt_extended import jwt_required, create_access_token,get_jwt_identity
from modelos import *
from flask import send_file

from tareas import *

usuario_schema = UsuarioSchema()
tarea_schema = TareaSchema()

'''
Login de un Usuario
'''
class VistaSignIn(Resource):
    @cross_origin()
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
                'access_token':access_token,
                 'usuario': usuario_schema.dump(usuario)
            }
        
        except:
            return {'message':'Ha ocurrido un error'}, 500

'''
Registro de un usuario
'''
class VistaSignUp(Resource):
    @cross_origin()
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
                'access_token': access_token,
                'usuario': usuario_schema.dump(nuevo_usuario)
            }

        except Exception as e:
            print(e)
            return {'message':'Ha ocurrido un error'}, 500            
   
    @cross_origin()
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
    Creación de una tarea de compresión
    '''
    @jwt_required()
    def post(self):
        file = request.files['file']
        
        nombre_arch, extension = os.path.splitext(file.filename)
        
        file.save('uploads/' + file.filename)
        usuario = Usuario.query.get_or_404(get_jwt_identity())
        email= usuario.email
        print('email',email)
        fecha_act= datetime.now()
        extension_convertir = request.form.get('extension_convertir')
        
        nueva_tarea= Tarea(
            nombre=request.form.get('nombre'),
            extension_original=extension,
            estado="uploaded",
            nombre_archivo_ori=nombre_arch,
            nombre_archivo_final=nombre_arch+"compressed",
            extension_convertir=request.form.get('extension_convertir'),
            fecha=fecha_act,
            usuarios=email
        )

        db.session.add(nueva_tarea)
        # tarea_en_cuest=Tarea.query.filter(Tarea.fecha==fecha_act).first()
        # print(tarea_en_cuest.fecha)
        if extension_convertir == ".zip":
            comprimir_zip.delay("uploads/"+nombre_arch+extension, nombre_arch+"compressed"+request.form.get('extension_convertir'), 'result', fecha_act)
        elif extension_convertir == ".gz":
            comprimir_gzip.delay("uploads/"+nombre_arch+extension, nombre_arch+"compressed"+request.form.get('extension_convertir'), 'result', fecha_act)
        elif extension_convertir == ".bz2":
            comprimir_bz2.delay("uploads/"+nombre_arch+extension, nombre_arch+"compressed"+request.form.get('extension_convertir'), 'result', fecha_act)
        else:
            return "Esta extensión no esta soportada en la aplicación"
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
    
class VistaFile(Resource):
    @jwt_required()
    def get(self,nombre_archivo):
        if "compressed" in nombre_archivo:
            task_con_archivo=[Tarea.query.filter(and_(Tarea.usuarios==get_jwt_identity(), or_(Tarea.nombre_archivo_final==nombre_archivo))).limit(1).all()]
            if len(task_con_archivo[0]) > 0:
                return send_file('result/'+nombre_archivo+task_con_archivo[0][0].extension_convertir)
            else:
                return "No se encontró ningún archivo relacionado a ninguna tarea del usuario"
        else:
            task_con_archivo=[Tarea.query.filter(and_(Tarea.usuarios==get_jwt_identity(), or_(Tarea.nombre_archivo_ori==nombre_archivo))).limit(1).all()]
            # print(task_con_archivo)
            if len(task_con_archivo[0]) > 0:
                return send_file('uploads/'+nombre_archivo+task_con_archivo[0][0].extension_original)
            else:
                return "No se encontró ningún archivo relacionado a ninguna tarea del usuario"

