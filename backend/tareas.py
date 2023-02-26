from celery import Celery
import zipfile
import bz2
import gzip
from modelos import *
import time

celery = Celery('tareas', broker='redis://localhost:6379/0')

@celery.task(name='comprimir_zip')
def comprimir_zip(filename, zipname, new_path,fecha_id):
    time.sleep(30)
    print("Antes")
    zfile = zipfile.ZipFile(new_path + '/' + zipname, 'w')
    zfile.write(filename, compress_type = zipfile.ZIP_DEFLATED)
    zfile.close()
    print("Despues")
    tarea_en_cuest=Tarea.query.filter(Tarea.fecha==fecha_id).first()
    tarea_en_cuest.estado = "processed"
    db.session.commit()

@celery.task(name='comprimir_gzip')
def comprimir_gzip(filename, zipname, new_path,fecha_id):
    time.sleep(30)
    print("Antes")
    old_file= open(filename)
    gzipFile = gzip.open(new_path + '/' + zipname, 'w')
    gzipFile.write(old_file.read())
    gzipFile.close()
    print("Despues")
    tarea_en_cuest=Tarea.query.filter(Tarea.fecha==fecha_id).first()
    tarea_en_cuest.estado = "processed"
    db.session.commit()

@celery.task(name='comprimir_bz2')
def comprimir_bz2(filename, zipname, new_path,fecha_id):
    time.sleep(30)
    print("Antes")
    old_file= open(filename)
    bz2File = open(new_path + '/' + zipname, 'w')
    bz2File.write(bz2.compress(old_file.read()))
    bz2File.close()
    print("Despues")
    tarea_en_cuest=Tarea.query.filter(Tarea.fecha==fecha_id).first()
    tarea_en_cuest.estado = "processed"
    db.session.commit()

