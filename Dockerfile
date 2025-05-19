# Usa como base una imagen de Python ligera con Python 3.10
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor en /app
WORKDIR /app

# Copia todos los archivos del directorio actual.
COPY . .

# Instala las dependencias del proyecto desde el archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 5000 para que pueda ser accedido desde fuera del contenedor.
EXPOSE 5000

# Comando que ejecuta al iniciar el contenedor.
CMD ["python", "manage.py"]



