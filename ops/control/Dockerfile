FROM python:3.12-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends docker.io \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY static/ static/

EXPOSE 8080
CMD ["uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8080"]
