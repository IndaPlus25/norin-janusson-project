from data.DTO_objects import TPMSSensorFormatted
from data.DB_models import TPMSSensor
from datetime import datetime
from collections import defaultdict


def format_sensor(sensor: TPMSSensor) -> TPMSSensorFormatted:
    obs_dict: dict[str, list[datetime]] = defaultdict(list)
    for obs in sensor.observations:
        obs_dict[obs.observation_sensor_id].append(obs.timestamp)
    return TPMSSensorFormatted(
        id=sensor.id,
        sensor_type=sensor.sensor_type,
        observations=dict(obs_dict),
    )
