¿Cómo ejecutar la aplicación?
Renombra y completa el archivo .env:
Renombra .env.example a .env.
Abre .env y añade tu GEMINI_API_KEY. Puedes dejar la SECRET_KEY y la DATABASE_URL como están para el entorno de desarrollo con Docker.
Verifica el modelo de IA de Gemini en el archivo app/main/routes.py
2.Abre una terminal y ejecuta Docker:

  docker-compose up --build

Este comando construirá la imagen de tu aplicación, descargará la imagen de PostgreSQL y lanzará ambos contenedores.
Inicializa la base de datos y crea el usuario administrador:
Abre una nueva terminal.
Ejecuta el siguiente comando para acceder al contenedor de la aplicación:


3.Inicializa la base de datos y crea el usuario administrador:
Abre una nueva terminal.
Ejecuta el siguiente comando para acceder al contenedor de la aplicación:

docker-compose exec web bash

Dentro del contenedor, ejecuta el comando para inicializar la base de datos.

FLASK_APP=run.py flask init-db


flask init-db


Esto creará las tablas y un usuario administrador con las siguientes credenciales:

Email: admin@agrocopilot.xyz
Contraseña: Mmipassword
Accede a la aplicación:
Abre tu navegador y ve a http://localhost:5000.
Inicia sesión con las credenciales del administrador y explora todas las funcionalidades.

docker-compose down

docker-compose up --build

docker-compose logs web





docker-compose up -d

docker-compose stop

docker-compose rm

docker-compose down -v

docker-compose logs

docker-compose build

docker-compose ps

docker-compose logs web
