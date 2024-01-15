FROM kartoza/postgis:latest
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASS=NdPYKnQLPKBZa7ZYeW9MA
ENV POSTGRES_DBNAME=masaveu_db

COPY ./init_data/*.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
EXPOSE 3232