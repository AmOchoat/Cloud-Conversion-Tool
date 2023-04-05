# Cloud-Entrega-3

Ejecición de la aplicación:

En la construcción de la solución se utilizaron 4 máquinas virtuales de Compute Engine y una instancia de Cloud SQL con postgres como manejador de bases de datos.

Todos estos elementos se encuentran conectados por una VPC que fue denominada "vpc-1". A continuación aclararemos las direciones de IP's privadas determinadas para cada instancia dentro de la VPC:
- Web-Server: 10.0.1.11
- Worker: 10.0.1.15
- NFS: 10.0.1.10

De la misma manera hay dos instancias con IP pública que permiten realizar conexión HTTP a través de puertos configurados previamente en las reglas de firewall:
- Front: 34.74.58.202
- Web-Server: 35.237.111.106

El repositorio de este proyecto fue clonado en cada una de las intancias mencionadas (Exceptuando Cloud SQL). A continuación se explicará el proceso de clonación y ejecución:
- Web-Server: 

      1. Clonar repo
      2. Instalar virtualenv a través de pip
      3. Pararse en la carpeta 'backend', crear y ejecutar el entorno virtual
      4. instalar todos los requerimientos del proyecto a través del comando: 'pip install -r requeriments.txt'
      5. ejecutar del backend en un servidor WGSI a través del comando 'gunicorn -b 0.0.0.0:8000 app:app'
      6. En otra consola pararse en la carpeta backed y ejecutar el comando: 'redis-server --protected-mode no' para iniciarlizar el message broker.
- Front:

      1. Clonar repo
      2. Instalar node.js
      3. Ejecutar el comando: 'sudo apt-get update && sudo apt-get install apache2 -y'
      4. Pararse en la carpeta front y ejecutar: 'npm install'
      6. Ejecutar el comando: 'npm run build'
      7. Copiar la build a la carpeta de apache: 'sudo cp -r Cloud-Entrega-1/front/build/* /var/www/html/'
      9. sudo /etc/init.d/apache2 restart
- Worker: 

      1. Clonar repo
      2. Instalar Celery a través de pip
      3. Pararse en la carpeta 'backend' y ejecutar el comando 'celery -A tareas worker -l info' para inicializar el worker
- NFS (https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-20-04-es):
    - En el host: 

		  1. sudo apt install nfs-kernel-server
		  2. sudo mkdir /var/nfs/general -p
		  3. sudo chown nobody:nogroup /var/nfs/general
		  4. sudo nano /etc/exports
    - En cada uno de los clientes (Las demás instancias): 

		  1. sudo apt install nfs-common
		  2. sudo mkdir -p /nfs/general
		  3. sudo mkdir -p /nfs/home
		  4. sudo mount host_ip:/var/nfs/general /nfs/general
		  5. sudo mount host_ip:/home /nfs/home
   

- Video Explicación: https://youtu.be/0Nk_Rx44LrM
- Documento de análisis de pruebas de carga: TODO
- Documento de arquitectura: TODO

Integrantes: 

- Andrés Ochoa 
- Esteban Ortiz
- Manuel Porras
- Daniel Jimenez
