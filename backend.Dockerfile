FROM python:3.12-slim

RUN apt-get update && apt-get upgrade -y

COPY requirements.txt .

RUN python3 -m venv /opt/venv && pip install -r requirements.txt

COPY backend .

CMD ["gunicorn", "app:app"]