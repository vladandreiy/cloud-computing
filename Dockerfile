FROM python:3.7-slim

WORKDIR /authentication_service

COPY requirements.txt /authentication_service/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /authentication_service/

CMD python authentication_service/manage.py runserver 0.0.0.0:8000
