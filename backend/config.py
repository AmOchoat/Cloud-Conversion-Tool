import os
from dotenv import load_dotenv

load_dotenv()
OUR_HOST = os.getenv("DB_HOST", "127.0.0.1")
OUR_DB = os.getenv("DB_DB", "tasks")
OUR_USER = os.getenv("DB_USER", "tasks")
OUR_PORT = os.getenv("DB_PORT", "5432")
OUR_PW = os.getenv("DB_PW", "tasks")
OUR_SECRET = os.getenv("SECRET", "tasks")
OUR_JWTSECRET = os.getenv("JWTSECRET", "tasks")
OUR_ALGO = os.getenv("JWT_ALGORITHM" ,"HS256")

DEBUG = False
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
    OUR_USER, OUR_PW, OUR_HOST, OUR_PORT, OUR_DB)

SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = OUR_JWTSECRET
SECRET_KEY = OUR_SECRET
JWT_ALGORITHM= OUR_ALGO