from __init__ import create_app
from flask_restful import Api
from modelos import *
from vistas import *
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin

app = create_app('default')
CORS(app)
cors = CORS(app, resource={
        r"/*":{
            "origins":"*"
        }
    })
app_context = app.app_context()
app_context.push()

db.init_app(app)

db.create_all() 
db.session.commit()
api = Api(app)

# Permite crear una cuenta de usuario, con los campos usuario, correo electrónico y 
# contraseña. El usuario y el correo electrónico deben ser únicos en la plataforma, la 
# contraseña debe seguir unos lineamientos mínimos de seguridad, además debe ser 
# solicitada dos veces para que el usuario confirme que ingresa la contraseña 
# correctamente. 

api.add_resource(VistaSignUp, '/api/auth/signup')

# Permite recuperar el token de autorización para consumir los recursos del API 
# suministrando un nombre de usuario y una contraseña correcta de una cuenta 
# registrada.
api.add_resource(VistaSignIn, '/api/auth/login')

# GET - Permite recuperar todas las tareas de conversión de un usuario autorizado en la 
# aplicación.
# 
# POST - Permite crear una nueva tarea de conversión de formatos. El usuario requiere 
# autorización.
api.add_resource(VistaTasks, '/api/tasks')

api.add_resource(VistaTask, '/api/task/<int:id_task>')

api.add_resource(VistaFile, '/api/files/<nombre_archivo>')

app.config['JWT_SECRET_KEY'] = "SuperSecret"
app.config["JWT_ALGORITHM"] = "HS256"
jwt = JWTManager(app)