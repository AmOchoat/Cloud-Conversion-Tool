# Cloud-Entrega-5

Ejecición de la aplicación:

Para este proyecto se crearon dos imágenes a partir del repositorio principal. Una imagen perteneciente al web-server y otra al worker. Estas imágenes fueron subidas a container registry y fueron usadas como imagen en Cloud Run

En el archivo dockerfile de web-server fue configurado para que se lanzara en el puerto 8000 por medio de un servidor WGSE. Y previamente se intalaron todas las dependencias necesarias para que corriera la aplicación flask.
En el archivo dockerfile de worker fue configurado para que se corriera el archivo tareas.py que escucha mediante la API de pub/sub los mensajes proveninetes de los susbriptores.

Tanto web-server como worker utilizan la API de pub/sub. Uno implementa la función enviar mensaje, el otro recibe el mensaje y lo confirma una vez se ha hecho el proceso de compresión. Estas peticiones se hacen a través de HTTP.

web-server y worker implementan la API de google cloud storage para guardar los archivos subidos y comprimidos. Cabe resaltar que para la conexión entre Cloud Run y Cloud SQL se implementó un VPC Connector que actúa como un puente entre la red de Cloud Run y la red VPC del proyecto.

En la construcción de la solución se utilizaron dos instancias de Cloud Run. 
	Instancia de web-sever: llamada img-proyecto2
	Instancia del worker: llamada pubsub-worker	


- Video Explicación: https://youtu.be/xPpVSL4b-hw
- Entrega 5 - Arquitectura, conclusiones y consideraciones: https://github.com/AmOchoat/Cloud-Conversion-Tool/blob/main/Entrega%205/Entrega%205%20-%20Arquitectura%2C%20conclusiones%20y%20consideraciones.pdf
- Plan de Pruebas y Analisis de Capacidad: https://github.com/AmOchoat/Cloud-Conversion-Tool/blob/main/Entrega%205/Plan%20de%20Pruebas%20y%20Analisis%20de%20Capacidad%20Entrega%205.pdf

Integrantes: 

- Andrés Ochoa 
- Esteban Ortiz
- Manuel Porras
- Daniel Jimenez
