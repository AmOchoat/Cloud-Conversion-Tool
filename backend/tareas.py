
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from google.cloud import pubsub_v1
from google.cloud import storage

import zipfile
import bz2
import gzip
from config import *


engine = create_engine(SQLALCHEMY_DATABASE_URI)

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
        new_path = mensaje_split[3]
        fecha_id = mensaje_split[4]
        
        # Ejecuta la tarea correspondiente
        if tarea == 'comprimir_zip':
            comprimir_zip(filename, zipname, new_path, fecha_id)
        if tarea == 'comprimir_gzip':
            comprimir_gzip(filename, zipname, new_path, fecha_id)
        if tarea == 'comprimir_bz2':
            comprimir_bz2(filename, zipname, new_path, fecha_id)

    
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


def comprimir_zip(filename, zipname, new_path,fecha_id):
    print("Comprimir zip")
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(filename)

    with blob.open('rb') as file:
        zfile = zipfile.ZipFile(new_path + '/' + zipname, 'w')
        zfile.writestr(filename, file.read(), compress_type=zipfile.ZIP_DEFLATED)
        zfile.close()

    zfile.write(filename, compress_type = zipfile.ZIP_DEFLATED)
    zfile.close()
    with engine.connect() as con:
        fecha_processed = fecha_id.replace("T", " ")        
        sentencia = f"UPDATE tarea SET estado = 'processed' WHERE fecha = '{fecha_processed}';"
        con.execute(text(sentencia))
        con.commit()
        
def comprimir_gzip(filename, zipname, new_path,fecha_id):
    print("Comprimir gzip")
    #old_file= open(filename)
    #gzipFile = gzip.open(new_path + '/' + zipname, 'w')
    #gzipFile.write(old_file.read())
    #gzipFile.close()
    #with engine.connect() as con:
    #    fecha_processed = fecha_id.replace("T", " ")
    #    sentencia = f"UPDATE tarea SET estado = 'processed' WHERE fecha = '{fecha_processed}';"
    #    con.execute(text(sentencia))
    #    con.commit()

def comprimir_bz2(filename, zipname, new_path,fecha_id):
    print("Comprimir bz2")
    #old_file= open(filename)
    #bz2File = open(new_path + '/' + zipname, 'w')
    #bz2File.write(bz2.compress(old_file.read()))
    #bz2File.close()
    #with engine.connect() as con:
    #    fecha_processed = fecha_id.replace("T", " ")
    #    sentencia = f"UPDATE tarea SET estado = 'processed' WHERE fecha = '{fecha_processed}';"
    #    con.execute(text(sentencia))
    #    con.commit()


if __name__ == "__main__":
    recibir_mensaje("compresion_archivo-sub")

