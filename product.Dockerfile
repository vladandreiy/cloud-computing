FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /business_logic

COPY requirements.txt /business_logic/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY business_logic /business_logic/

COPY create-dbs.sh /docker-entrypoint-initdb.d/

CMD python manage.py makemigrations; python manage.py migrate; python manage.py runserver 0.0.0.0:8000