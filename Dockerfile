FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /authentication_service

COPY requirements.txt /authentication_service/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    gunicorn

COPY . /authentication_service/

CMD gunicorn authentication_service.wsgi:application --bind 0.0.0.0:7000