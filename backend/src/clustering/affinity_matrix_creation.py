from datetime import datetime

import numpy as np
from numpy.typing import NDArray

from data.DTO_objects import ObservationResponseDto, TPMSSensorResponseDto


def add_observation_coocurence(
    base_matrix: NDArray[np.float64],
    tpms_sensor_dict: dict[int, TPMSSensorResponseDto],
    observation_dict: dict[int, ObservationResponseDto],
) -> NDArray[np.float64]:
    sensor_count = len(tpms_sensor_dict)

    for i in range(0, sensor_count):
        sensor_i = tpms_sensor_dict.get(i)
        if sensor_i is None:
            raise ValueError(
                f"Can't get tpms sensor since key {i} does not exist in tpms sensor dictionary"
            )

        for i2 in range(i + 1, sensor_count):
            sensor_j = tpms_sensor_dict.get(i2)
            if sensor_j is None:
                raise ValueError(
                    f"Can't get tpms sensor since key {i2} does not exist in tpms sensor dictionary"
                )

            obs_i_by_sensor: dict[str, list[datetime]] = {}
            for obs_id in sensor_i.observation_ids:
                obs = observation_dict[obs_id]
                obs_i_by_sensor.setdefault(obs.observation_sensor_id, []).append(
                    obs.timestamp
                )

            obs_j_by_sensor: dict[str, list[datetime]] = {}
            for obs_id in sensor_j.observation_ids:
                obs = observation_dict[obs_id]
                obs_j_by_sensor.setdefault(obs.observation_sensor_id, []).append(
                    obs.timestamp
                )

            matches = 0
            for sensor_id, timestamps_i in obs_i_by_sensor.items():
                timestamps_j = obs_j_by_sensor.get(sensor_id)
                if timestamps_j is None:
                    continue
                matches += _count_matches(timestamps_i, timestamps_j)

            base_matrix[i][i2] += matches
            base_matrix[i2][i] += matches

    return base_matrix


def add_blacklist(
    base_matrix: NDArray[np.float64], black_list: NDArray[np.bool_]
) -> NDArray[np.float64]:
    base_matrix[~black_list] = 0
    return base_matrix


def _count_matches(arr1: list[datetime], arr2: list[datetime]) -> int:
    count = 0
    for dt1 in arr1:
        for dt2 in arr2:
            if abs((dt1 - dt2).total_seconds()) <= 60:
                count += 1
    return count


def add_sensor_type_coocurence(
    base_matrix: NDArray[np.float64], tpms_sensors: list[TPMSSensorResponseDto]
) -> NDArray[np.float64]:
    sensor_count = len(tpms_sensors)
    for i in range(sensor_count):
        for j in range(i + 1, sensor_count):
            if tpms_sensors[i].sensor_type == tpms_sensors[j].sensor_type:
                base_matrix[i][j] += 1
                base_matrix[j][i] += 1
    return base_matrix
