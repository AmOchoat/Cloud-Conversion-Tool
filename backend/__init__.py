from flask import Flask
from flask_cors import CORS

def create_app(config_name):
    app = Flask(__name__)  
    cors = CORS(app, resource={
        r"/*":{
            "origins":"*"
        }
    })
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://tasks:tasks@localhost/tasks'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['JWT_SECRET_KEY']='tasks'
    app.config['PROPAGATE_EXCEPTIONS']=True

    return app