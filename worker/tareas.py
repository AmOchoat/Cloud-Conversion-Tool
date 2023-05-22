from sqlalchemy.sql import text
from sqlalchemy import create_engine
from google.cloud import storage
import base64
from flask import Flask, request


app = Flask(__name__)


import zipfile
import bz2
import gzip
from io import BytesIO

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

engine = create_engine(SQLALCHEMY_DATABASE_URI)

storage_client = storage.Client.from_service_account_json("entrega-3-CloudStorage.json")
bucket_name = "cloud-entrega-4"


@app.route("/", methods=["POST"])
def recibir_mensaje():

    
    envelope = request.get_json()
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]

    name = "World"
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        name = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()

        # Extrae los parámetros de la tarea del mensaje
        mensaje_split = name.split(' ')
        tarea = mensaje_split[0]
        filename = mensaje_split[1]
        zipname = mensaje_split[2]
        fecha_id = mensaje_split[3]
        
        # Ejecuta la tarea correspondiente
        if tarea == 'comprimir_zip':
            comprimir_zip(bucket_name, filename, zipname, fecha_id)
        elif tarea == 'comprimir_gzip':
            comprimir_gzip(filename, zipname, bucket_name, fecha_id)
        elif tarea == 'comprimir_bz2':
            comprimir_bz2(filename, zipname, bucket_name, fecha_id)

    return ("", 204)


def comprimir_zip(bucket_name, filename, zipname, fecha_id):
    bucket = storage_client.get_bucket(bucket_name)

    print("zipname:", zipname)
    print("filename:", filename)
    
    blob = bucket.blob(filename)
    
    with BytesIO() as zip_buffer:
        with zipfile.ZipFile(zip_buffer, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
            data = blob.download_as_string()
            zip_file.writestr(filename, data)

        blob_zip = bucket.blob(zipname)
        blob_zip.upload_from_string(zip_buffer.getvalue())

    with engine.connect() as con:
        fecha_processed = fecha_id.replace("T", " ")
        sentencia = f"UPDATE tarea SET estado = 'processed' WHERE fecha = '{fecha_processed}';"
        con.execute(text(sentencia))
        con.commit()
        
def comprimir_gzip(bucket_name, filename, zipname, fecha_id):
    bucket = storage_client.get_bucket(bucket_name)

    print("zipname:", zipname)
    print("filename:", filename)


    blob = bucket.blob(filename)

    with BytesIO() as zip_buffer:
        with gzip.GzipFile(mode='wb', fileobj=zip_buffer) as zip_file:
            data = blob.download_as_string()
            zip_file.write(data)

        blob_zip = bucket.blob(zipname)
        blob_zip.upload_from_string(zip_buffer.getvalue())

    with engine.connect() as con:
        fecha_processed = fecha_id.replace("T", " ")
        sentencia = f"UPDATE tarea SET estado = 'processed' WHERE fecha = '{fecha_processed}';"
        con.execute(text(sentencia))
        con.commit()


def comprimir_bz2(bucket_name, filename, zipname, fecha_id):

    bucket = storage_client.get_bucket(bucket_name)

    print("zipname:", zipname)
    print("filename:", filename)


    blob = bucket.blob(filename)

    with BytesIO() as zip_buffer:
        with bz2.BZ2File(mode='wb', filename=zip_buffer) as zip_file:
            data = blob.download_as_string()
            zip_file.write(data)

        blob_zip = bucket.blob(zipname)
        blob_zip.upload_from_string(zip_buffer.getvalue())

    with engine.connect() as con:
        fecha_processed = fecha_id.replace("T", " ")
        sentencia = f"UPDATE tarea SET estado = 'processed' WHERE fecha = '{fecha_processed}';"
        con.execute(text(sentencia))
        con.commit()