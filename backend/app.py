from backend import create_app
from flask_restful import Api
from .modelos import db
from .vistas import *
from flask_jwt_extended import JWTManager

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)

api.add_resource(VistaSignIn, '/api/auth/login')
api.add_resource(VistaSignUp, '/api/auth/signup')
api.add_resource(VistaTasks, '/api/tasks')
api.add_resource(VistaTask, '/api/tasks/<int:id_task>')

jwt = JWTManager(app)