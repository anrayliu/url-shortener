FROM postgres:18.1-alpine

COPY backend/init.sql /docker-entrypoint-initdb.d/init.sql
