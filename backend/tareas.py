from celery import Celery
from sqlalchemy.sql import text
from sqlalchemy import create_engine

import zipfile
import bz2
import gzip
from config import *

celery = Celery('tareas', broker='redis://10.0.1.11:6379/0')
engine = create_engine(SQLALCHEMY_DATABASE_URI)

@celery.task(name='comprimir_zip')
def comprimir_zip(filename, zipname, new_path,fecha_id):
    zfile = zipfile.ZipFile(new_path + '/' + zipname, 'w')
    zfile.write(filename, compress_type = zipfile.ZIP_DEFLATED)
    zfile.close()
    with engine.connect() as con:
        sentencia = f"UPDATE tarea SET estado = 'processed' WHERE fecha = '{fecha_id}';"
        result = con.execute(text(sentencia))
        print(result)
        
@celery.task(name='comprimir_gzip')
def comprimir_gzip(filename, zipname, new_path,fecha_id):
    old_file= open(filename)
    gzipFile = gzip.open(new_path + '/' + zipname, 'w')
    gzipFile.write(old_file.read())
    gzipFile.close()
    with engine.connect() as con:
        sentencia = f"UPDATE tarea SET estado = 'processed' WHERE fecha = '{fecha_id}';"
        result = con.execute(text(sentencia))
        print(result)

@celery.task(name='comprimir_bz2')
def comprimir_bz2(filename, zipname, new_path,fecha_id):
    old_file= open(filename)
    bz2File = open(new_path + '/' + zipname, 'w')
    bz2File.write(bz2.compress(old_file.read()))
    bz2File.close()
    with engine.connect() as con:
        sentencia = f"UPDATE tarea SET estado = 'processed' WHERE fecha = '{fecha_id}';"
        result = con.execute(text(sentencia))
        print(result)
