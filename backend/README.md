### CORRER BACKEND

1. Crear ambiente python3 -m venv env
2. Iniciar ambiente source env/bin/activate
3. Instalar dependencias pip install -r requirements.txt
4. Instalar postgres https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart
5. Crear base de datos con nombre tasks y un usuario y clave tasks.
https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application
6. Instalación y ejecución de de Redis y Celery.
  Para la ejecución de Celery hacer uso del comando `celery -A tareas worker -l info`.
