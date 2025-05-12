# Imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py app.py

# Expone el puerto que Flask usará
EXPOSE 5000

# Comando por defecto para ejecutar la app
CMD ["python", "app.py"]
