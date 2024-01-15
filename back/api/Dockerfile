FROM --platform=linux/x86_64 python:3.10.4-buster

# INSTALL DOCKERIZE
RUN apt-get update && apt-get install -y wget
RUN apt-get install -y gdal-bin libgdal-dev
RUN apt-get install -y iputils-ping
RUN apt-get install -y gettext
RUN apt-get install -y curl
RUN apt-get install -y netcat

#FOR SQL CONNECTION
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | tee /etc/apt/sources.list.d/msprod.list
RUN apt-get update 
RUN ACCEPT_EULA=y apt-get install -y mssql-tools -y unixodbc-dev

EXPOSE 8000

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /api
ENV API_ADMIN_USER admin
ENV API_ADMIN_PASSWORD test_admin

ENV POSTGRES_HOST postgis
ENV POSTGRES_PORT 5432
ENV POSTGRES_DB masaveu_db
ENV POSTGRES_USER postgres
ENV POSTGRES_PASS NdPYKnQLPKBZa7ZYeW9MA

ENV DEBUG 1


ENV SECRET_KEY i1b1y8g1ggb8iu1gw9p8e145r6tfvujhkjknly8w7etr78wetr7wegfvbywevb09wy9qw09r8gfiabvsnkcmxoqk9089w7t


RUN mkdir /var/run/gunicorn
RUN mkdir /var/log/gunicorn
RUN mkdir /api
RUN mkdir /api/staticfiles
RUN mkdir /api/media
COPY /media /api/media
WORKDIR /api
COPY requirements.txt /api/
RUN pip install -r requirements.txt

COPY . /api/
WORKDIR /







