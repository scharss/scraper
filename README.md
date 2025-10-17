# AI Web Scraper
## 🐳 Docker Installation

The application uses Docker to work consistently across all platforms. Follow these instructions to install it on your system.

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/)
- [Docker Compose](https://docs.docker.com/compose/install/) (included in Docker Desktop for Windows and Mac)
- At least 8GB of available RAM
- Approximately 10GB of disk space (varies depending on the models you download)

### 🪟 Windows Installation

1. **Install Docker Desktop**:
   - Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
   - Install WSL 2 if necessary (Windows 10/11):
     ```powershell
     wsl --install
     ```
   - Run the Docker Desktop installer and make sure the "Use WSL 2" option is selected
   - Restart your computer
### 🍎 macOS Installation

1. **Install Docker Desktop**:
   - Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
   - Run the installer (make sure to select the correct version for your Mac: Intel or Apple Silicon)

2. **Clone/Download the Repository**:
   ```bash
   git clone https://github.com/scharss/bytecrafterassistant.git
   cd bytecrafterassistant
   ```
   Or download and extract the repository ZIP

3. **Start the Containers**:
   ```bash
   docker-compose up -d
   ```
### 🐧 Linux Installation

1. **Install Docker and Docker Compose**:
   - Ubuntu/Debian:
     ```bash
     sudo apt update
     sudo apt install docker.io docker-compose
     sudo systemctl enable --now docker
     ```
   - Fedora/RHEL/CentOS:
     ```bash
     sudo dnf install docker docker-compose
     sudo systemctl enable --now docker
     ```
   - Arch Linux:
     ```bash
     sudo pacman -S docker docker-compose
     sudo systemctl enable --now docker
     ```

2. **Add Your User to the Docker Group** (to use Docker without sudo):
   ```bash
   sudo usermod -aG docker $USER
   ```
   Log out and back in for the changes to take effect.
¿Cómo ejecutar la aplicación?
Renombra y completa el archivo .env:
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
