# Imagen base oficial Python slim (liviana y segura)
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias primero (aprovecha caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Puerto interno de Gunicorn
EXPOSE 5000

# Arrancar Gunicorn como servidor WSGI
# -w 2        → 2 workers (suficiente para laboratorio)
# -b 0.0.0.0:5000 → escuchar en todos los interfaces
# wsgi:application → archivo wsgi.py, objeto 'application'
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "wsgi:application"]
