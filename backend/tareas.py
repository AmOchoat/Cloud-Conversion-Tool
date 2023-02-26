from celery import Celery
import zipfile
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
