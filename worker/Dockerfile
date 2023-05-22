FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y

# Instalar Python3 y otras dependencias necesarias
RUN apt-get install -y python3 python3-pip libpq-dev python3-dev vim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY . /app
COPY .env /app

# Instalar dependencias
RUN pip3 install --no-cache-dir -r requirements.txt

COPY tareas.py ./

# Agregar servidor Gunicorn como punto de entrada
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 tareas:app
