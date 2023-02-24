from celery import Celery
import zipfile

celery = Celery('tareas', broker='redis://localhost:6379/0')

@celery.task(name='comprimir_zip')
def comprimir_zip(filename, zipname, new_path):
    zfile = zipfile.ZipFile(new_path + '/' + zipname, 'w')
    zfile.write(filename, compress_type = zipfile.ZIP_DEFLATED)
    zfile.close()