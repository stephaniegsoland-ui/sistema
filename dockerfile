# Imagen base de Python 3.12
FROM python:3.12-slim

# Evita que Python genere archivos .pyc y permite ver logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalamos dependencias del sistema necesarias para Reflex y MySQL
RUN apt-get update && apt-get install -y \
    unzip \
    curl \
    libmariadb-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiamos e instalamos las librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el proyecto (excepto lo que esté en .dockerignore)
COPY . .

# Inicializamos Reflex para descargar Bun y dependencias de JS
RUN reflex init

# Exponemos puertos de Frontend y Backend
EXPOSE 3000 8000

# Comando para arrancar en modo desarrollo
CMD ["reflex", "run", "--env", "dev"]