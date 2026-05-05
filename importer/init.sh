#!/bin/bash
set -e


until pg_isready -h /var/run/postgresql -U postgres; do
  sleep 2
done

OSM_XML=/tmp/osm-input.osm

echo "Converting PBF to OSM XML..."
osmium cat -o "$OSM_XML" --overwrite /sweden.osm.pbf

osm2pgrouting \
  --file "$OSM_XML" \
  --dbname gis \
  --username postgres \
  --password postgres \
  --host /var/run/postgresql \
  --clean

rm -f "$OSM_XML"
echo "Import complete."