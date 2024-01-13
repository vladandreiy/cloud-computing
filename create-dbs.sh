#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER ccstudent WITH PASSWORD '123';
    CREATE DATABASE ccdb;
    GRANT ALL PRIVILEGES ON DATABASE ccdb TO ccstudent;
EOSQL