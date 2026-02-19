# While this copy can be made in compose.yaml, I'm still keeping a Dockerfile for the database
# to respect the 3-tier architecture


FROM postgres:18.1

# removes bin for CVE-2025-68121
# see https://github.com/docker-library/postgres/issues/1324 and attached pr for details
RUN rm -rf /usr/local/bin/gosu

COPY backend/database/init.sql /docker-entrypoint-initdb.d/init.sql
