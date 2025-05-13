# FROM python:3.11-slim


# WORKDIR /aplicacion


# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 5000

# CMD ["python", "manage.py"]

# Imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos de requerimientos (si tienes uno)
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código de la aplicación
COPY . .

# Expón el puerto 5000 (aunque usarás socket con Nginx si lo deseas)
EXPOSE 5000

# Ejecuta la app usando gunicorn (WSGI), necesario para producción
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "aplicacion.app:app"]


