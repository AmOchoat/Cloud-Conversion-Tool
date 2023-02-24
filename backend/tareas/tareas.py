from celery import Celery
from zipfile import ZipFile
from .zip import compress

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def comprimir_zip(filename, zipname, new_path):
    compress(filename, zipname, new_path)