FROM postgres:10.4
COPY init.sql /docker-entrypoint-initdb.d/