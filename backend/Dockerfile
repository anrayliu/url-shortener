FROM python:3.12-slim

RUN apt-get update && apt-get upgrade -y

WORKDIR /app

COPY requirements.txt .

RUN python3 -m venv /opt/venv && pip install --no-cache-dir -r requirements.txt

COPY backend .

CMD ["gunicorn", "app:app"]
