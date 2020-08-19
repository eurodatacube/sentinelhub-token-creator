FROM python:3.8.1-slim

WORKDIR /srv/service
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ADD . .

USER www-data

CMD ["gunicorn", "--bind=0.0.0.0:8080", "--workers=3", "--log-level=INFO", "app:app"]