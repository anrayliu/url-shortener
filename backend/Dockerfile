FROM python:3.12-slim

# update container packages
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# install python packages
RUN python3 -m venv /opt/venv && pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# run as non-root user
RUN useradd -m appuser
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
