FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y

# Intalar Python3
RUN apt-get install -y python3 python3-pip

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY . /app

COPY .env /app

# Instalar psycopg2-binary
RUN apt install libpq-dev python3-dev -y

# Instalar dependencias
RUN pip3 install --no-cache-dir -r requirements.txt

# Ejecutar con gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]