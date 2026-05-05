FROM pgrouting/pgrouting

RUN apt-get update && apt-get install -y \
    osm2pgrouting \
    osmium-tool \
    && rm -rf /var/lib/apt/lists/*

COPY init.sh /docker-entrypoint-initdb.d/002_init.sh
RUN chmod +x /docker-entrypoint-initdb.d/002_init.sh