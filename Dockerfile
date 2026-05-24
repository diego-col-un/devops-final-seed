FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias de seguridad del sistema si es necesario
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Seguridad: No correr como root
RUN useradd -m devopsuser && chown -R devopsuser:devopsuser /app
USER devopsuser

EXPOSE 5000

CMD ["python", "src/app.py"]