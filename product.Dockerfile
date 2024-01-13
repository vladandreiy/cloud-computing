FROM python:3.7-slim

WORKDIR /business_logic

COPY requirements.txt /business_logic/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /business_logic/

COPY create-dbs.sh /docker-entrypoint-initdb.d/

CMD python business_logic/manage.py makemigrations; python business_logic/manage.py migrate; python business_logic/manage.py runserver 0.0.0.0:8000