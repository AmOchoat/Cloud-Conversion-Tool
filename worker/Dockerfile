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

CMD ["python3", "tareas.py"]
