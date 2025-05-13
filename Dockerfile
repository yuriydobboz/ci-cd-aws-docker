# Usa una imagen oficial de Python
FROM python:3.10-slim

# Crea un directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todo el contenido del proyecto a /app en el contenedor
#COPY . .
COPY manage.py /app
COPY templates /aplicacion/templates


# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expón el puerto por el que correrá la app
EXPOSE 5000

# Comando para ejecutar la app (usando manage.py)
CMD ["python", "manage.py"]



