# Pull official base image
FROM postgres:12.1-alpine

# Run create.sql / create database on init
ADD create.sql /docker-entrypoint-initdb.d
