# Cloud-Entrega-4

Ejecición de la aplicación:

En la construcción de la solución se utilizaron tres grupos de instancias. 
	Grupos de instancias de web-sever:
		- instance-group-uno. Contiene al Web server en la zona us-east1-b
		- instance-group-dos. Contiene al Web server en la zona us-east1-c
	Grupos de instancias de worker:
		- instance-group-workers. Contiene al Worker en la zona us-east1-b	

Load balancer:
	web-server-lb: Tiene asociados los dos grupos de instancias del web-server y redirige a sus repectivas IPs para hacer peticiones a la API. 
		- IP del balanceador: 34.160.186.126. Esta IP es pública.


Para este proyecto se crearon dos imágenes a partir del repositorio principal. Una imagen perteneciente al web-server y otra al worker. Estas imágenes fueron subidas a container registry y fueron usadas como imagen en nuestras instance template para lanzar nuestros grupos de instancias de web-server y worker.

En el archivo dockerfile de web-server fue configurado para que se lanzara en el puerto 8000 por medio de un servidor WGSE. Y previamente se intalaron todas las dependencias necesarias para que corriera la aplicación flask.

En el archivo dockerfile de worker fue configurado para que se corriera el archivo tareas.py que escucha mediante la API de pub/sub los mensajes proveninetes de los susbriptores.

Tanto web-server como worker utilizan la API de pub/sub. Uno implementa la finción enviar mensaje, el otro recibe el mensaje y lo confirma una vez se ha hecho el proceso de compresión.

web-server y worker implementan la API de google cloud storage para guardar los archivos subidos y comprimidos.

- Video Explicación: https://www.youtube.com/watch?v=VZXf26EIiCk
- Entrega 4 - Arquitectura, conclusiones y consideraciones: https://github.com/AmOchoat/Cloud-Entrega-1/blob/main/Entrega%204/Entrega%204%20-%20Arquitectura%2C%20conclusiones%20y%20consideraciones.pdf
- Plan de Pruebas y Analisis de Capacidad: https://github.com/AmOchoat/Cloud-Entrega-1/blob/main/Entrega%204/Plan%20de%20Pruebas%20y%20Analisis%20de%20Capacidad%20Entrega%204.pdf

Integrantes: 

- Andrés Ochoa 
- Esteban Ortiz
- Manuel Porras
- Daniel Jimenez
