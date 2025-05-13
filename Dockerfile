# Usa Python slim como base
FROM python:3.11-slim

# Define directorio de trabajo
WORKDIR /app

# Copia requisitos y proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expón el puerto
EXPOSE 5000

# Comando de inicio
CMD ["python", "manage.py"]
