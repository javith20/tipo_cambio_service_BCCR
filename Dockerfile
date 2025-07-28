FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expone el puerto de FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]