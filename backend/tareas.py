
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from google.cloud import pubsub_v1
from google.cloud import storage

import zipfile
import bz2
import gzip
from config import *
from io import BytesIO


#engine = create_engine(SQLALCHEMY_DATABASE_URI)

storage_client = storage.Client()
bucket_name = "cloud-entrega-4"

def recibir_mensaje(pubsub_subscription):
    # Crea una instancia del cliente de Pub/Sub con las credenciales
    subscriber = pubsub_v1.SubscriberClient.from_service_account_json("pub_sub.json")
    
    # Crea una función de callback para procesar los mensajes recibidos
    def callback(message):
        # Extrae los parámetros de la tarea del mensaje
        mensaje_split = message.data.decode().split(' ')
        tarea = mensaje_split[0]
        filename = mensaje_split[1]
        zipname = mensaje_split[2]
        fecha_id = mensaje_split[3]
        
        # Ejecuta la tarea correspondiente
        if tarea == 'comprimir_zip':
            comprimir_zip(bucket_name, filename, zipname, fecha_id)
        if tarea == 'comprimir_gzip':
            comprimir_gzip(filename, zipname, bucket_name, fecha_id)
        if tarea == 'comprimir_bz2':
            comprimir_bz2(filename, zipname, bucket_name, fecha_id)

    
    # Crea una instancia de suscripción
    subscription_path = subscriber.subscription_path("entrega-3-cloud", pubsub_subscription)
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    
    # Inicia el bucle de recepción de mensajes
    with subscriber:
        try:
            # Espera hasta que se cierre el futuro de recepción de mensajes
            streaming_pull_future.result()
        except Exception as e:
            # Maneja cualquier error ocurrido durante la recepción de mensajes
            print(f'Error al recibir mensajes: {e}')


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

    #with engine.connect() as con:
        #fecha_processed = fecha_id.replace("T", " ")
        #sentencia = f"UPDATE tarea SET estado = 'processed' WHERE fecha = '{fecha_processed}';"
        #con.execute(text(sentencia))
        #con.commit()
        
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

    #with engine.connect() as con:
        #fecha_processed = fecha_id.replace("T", " ")
        #sentencia = f"UPDATE tarea SET estado = 'processed' WHERE fecha = '{fecha_processed}';"
        #con.execute(text(sentencia))
        #con.commit()


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

    #with engine.connect() as con:
        #fecha_processed = fecha_id.replace("T", " ")
        #sentencia = f"UPDATE tarea SET estado = 'processed' WHERE fecha = '{fecha_processed}';"
        #con.execute(text(sentencia))
        #con.commit()


if __name__ == "__main__":
    recibir_mensaje("compresion_archivo-sub")

