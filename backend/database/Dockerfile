# While this copy can be made in compose.yaml, I'm still keeping a Dockerfile for the database
# to respect the 3-tier architecture


FROM postgres:18.1

# not needed and has a vulnerability
RUN rm -rf /usr/local/bin/gosu

COPY backend/database/init.sql /docker-entrypoint-initdb.d/init.sql
