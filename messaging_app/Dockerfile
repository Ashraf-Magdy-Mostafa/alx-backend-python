# messaging_app/Dockerfile
FROM python:3.10-slim

# 1) System deps (add build tools only if you need them)
RUN apt-get update && apt-get install -y --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

# 2) Create non-root user (best practice)
RUN useradd -m appuser
WORKDIR /app

# 3) Copy only requirements first to leverage layer caching
COPY requirements.txt /app/

# 4) Install Python deps (no cache -> smaller image)
RUN pip install --no-cache-dir -r requirements.txt

# 5) Copy project code
COPY . /app

# 6) Environment (avoid writing pyc; unbuffered logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 7) Expose Django’s default port
EXPOSE 8000

# 8) Healthcheck (optional, nice to have)
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import socket; s=socket.socket(); s.settimeout(2); s.connect(('127.0.0.1', 8000))" || exit 1

# 9) Runserver for DEV; swap to gunicorn for PROD
# If your Django settings module isn’t the default, set it via env at runtime
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
