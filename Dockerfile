# Usamos Ubuntu como base
FROM ubuntu:latest

# Instalamos Python, PIP y Venv (necesario en Ubuntu nuevos)
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Creamos un entorno virtual para instalar librerías sin errores
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instalamos psutil
RUN pip install psutil

# Preparamos la carpeta de trabajo
WORKDIR /app

# Copiamos TUS archivos al contenedor
COPY servidor.py gestor.py /app/

# Comando que se ejecuta al iniciar el contenedor
CMD ["python3", "servidor.py"]
