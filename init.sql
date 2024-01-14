CREATE DATABASE ccdb;
DO
$BODY$
BEGIN
   IF NOT EXISTS (
      SELECT *
      FROM   pg_catalog.pg_user
      WHERE  usename = 'ccstudent') THEN

      CREATE USER ccstudent WITH PASSWORD '123';
   END IF;
END
$BODY$;
GRANT ALL PRIVILEGES ON DATABASE ccdb TO ccstudent;