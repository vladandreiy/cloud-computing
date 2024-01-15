FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /authentication_service

COPY requirements.txt /authentication_service/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY authentication_service /authentication_service/

CMD python manage.py makemigrations; python manage.py migrate; python manage.py runserver 0.0.0.0:7000