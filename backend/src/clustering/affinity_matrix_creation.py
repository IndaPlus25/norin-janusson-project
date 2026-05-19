from collections import defaultdict

import numpy as np
from numpy.typing import NDArray
from config import TPMS_CLUSTER_WINDOW

from data.dtos import ObservationResponseDto, TPMSSensorResponseDto


def add_observation_coocurence(
    base_matrix: NDArray[np.float64],
    tpms_sensor_dict: dict[int, TPMSSensorResponseDto],
    observations: list[ObservationResponseDto],
) -> NDArray[np.float64]:
    if base_matrix.size == 0 or not observations:
        return base_matrix

    tpms_id_to_index: dict[str, int] = {
        sensor.id: index for index, sensor in tpms_sensor_dict.items()
    }

    grouped: dict[str, list[ObservationResponseDto]] = defaultdict(list)
    for obs in observations:
        if obs.tpms_sensor_id in tpms_id_to_index:
            grouped[obs.observation_sensor_id].append(obs)

    pair_counts: dict[tuple[int, int], int] = defaultdict(int)
    window = float(TPMS_CLUSTER_WINDOW)

    for group in grouped.values():
        group.sort(key=lambda o: o.received_at)
        n = len(group)
        for i in range(n):
            anchor = group[i]
            anchor_index = tpms_id_to_index[anchor.tpms_sensor_id]
            for j in range(i + 1, n):
                candidate = group[j]
                gap = (candidate.received_at - anchor.received_at).total_seconds()
                if gap > window:
                    break
                if anchor.tpms_sensor_id == candidate.tpms_sensor_id:
                    continue
                candidate_index = tpms_id_to_index[candidate.tpms_sensor_id]
                key = (
                    (anchor_index, candidate_index)
                    if anchor_index < candidate_index
                    else (candidate_index, anchor_index)
                )
                pair_counts[key] += 1

    for (i, j), count in pair_counts.items():
        base_matrix[i][j] += count
        base_matrix[j][i] += count

    return base_matrix


def add_blacklist(
    base_matrix: NDArray[np.float64], black_list: NDArray[np.bool_]
) -> NDArray[np.float64]:
    base_matrix[~black_list] = 0
    return base_matrix


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
