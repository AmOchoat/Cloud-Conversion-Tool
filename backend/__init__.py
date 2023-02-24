from flask import Flask
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app(config_name):
    app = Flask(__name__)  
    CORS(app)
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