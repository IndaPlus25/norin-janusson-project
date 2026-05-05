import os

import psycopg
from fastapi import APIRouter, Depends

from data.DTO_objects import CreateObservationSensorDto, ObservationSensorResponseDto
from db.DB_ops import (
    create_observation_sensor,
    get_all_observation_sensors,
    get_observation_sensor,
)


def get_pg_conn():
    dsn = os.environ["PG_DSN"]
    with psycopg.connect(dsn) as conn:
        yield conn


router = APIRouter(tags=["trajectory_inference"])


@router.get(
    "/trajectory_inference",
    response_model=list[ObservationSensorResponseDto],
)
def list_observation_sensors():
    return get_all_observation_sensors()


@router.get("/route")
def route(conn: psycopg.Connection = Depends(get_pg_conn)):
    lon1: float = 18.06
    lat1: float = 59.33
    lon2: float = 18.07
    lat2: float = 59.34
    with conn.cursor() as cur:
        cur.execute("""
            WITH
            start_node AS (
                SELECT id
                FROM ways_vertices_pgr
                ORDER BY the_geom <-> ST_SetSRID(ST_Point(%s, %s), 4326)
                LIMIT 1
            ),
            end_node AS (
                SELECT id
                FROM ways_vertices_pgr
                ORDER BY the_geom <-> ST_SetSRID(ST_Point(%s, %s), 4326)
                LIMIT 1
            )

            SELECT ST_AsGeoJSON(
                ST_LineMerge(ST_Union(w.the_geom))
            ) AS geojson

            FROM pgr_dijkstra(
                'SELECT gid AS id, source, target, cost FROM ways',
                (SELECT id FROM start_node),
                (SELECT id FROM end_node),
                directed := false
            ) AS r
            JOIN ways w ON r.edge = w.gid;
        """, (lon1, lat1, lon2, lat2))

        row = cur.fetchone()
        return {"route": row[0] if row else None}
