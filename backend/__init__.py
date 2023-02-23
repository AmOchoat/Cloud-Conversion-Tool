from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

jwt = JWTManager()

def create_app(config_name):
    app = Flask(__name__)  
    cors = CORS(app, resource={
        r"/*":{
            "origins":"*"
        }
    })
    try:
        app.config.from_pyfile('config.py')
    except:
        pass

    jwt.init_app(app)

    return app