from collections import defaultdict

import numpy as np
from numpy.typing import NDArray

from data.DTO_objects import (
    CreateCarDto,
    CreateCarObservationDto,
    ObservationResponseDto,
    TPMSSensorResponseDto,
)


def affinity_to_euclidian(affinity_matrix: NDArray[np.float64]) -> NDArray[np.float64]:
    return 1 - affinity_matrix


def get_empty_base_matrix(
    tpms_sensors: list[TPMSSensorResponseDto],
) -> tuple[NDArray[np.float64], dict[int, TPMSSensorResponseDto]]:
    tpms_sensor_dict: dict[int, TPMSSensorResponseDto] = {
        i: tpms_sensor for i, tpms_sensor in enumerate(tpms_sensors)
    }
    matrix_size = len(tpms_sensors)
    base_matrix = np.zeros((matrix_size, matrix_size), dtype=np.float64)
    return (base_matrix, tpms_sensor_dict)


def get_observation_dict(
    observations: list[ObservationResponseDto],
) -> dict[int, ObservationResponseDto]:
    return {observation.id: observation for observation in observations}


def get_sub_cluster_matrix(
    affinity_matrix: NDArray[np.float64], sub_cluster: list[int]
) -> tuple[NDArray[np.float64], dict[int, int]]:
    cluster_map_dict: dict[int, int] = {
        sub_cluster_pos: cluster_pos
        for sub_cluster_pos, cluster_pos in enumerate(sub_cluster)
    }
    indices = np.array(sub_cluster, dtype=int)
    sub_cluster_matrix = affinity_matrix[np.ix_(indices, indices)]
    return (sub_cluster_matrix, cluster_map_dict)


def create_car_observations(
    observations: list[ObservationResponseDto], cars: list[CreateCarDto]
) -> list[CreateCarObservationDto]:

    tpms_to_car_index: dict[str, int] = {}
    for index, car in enumerate(cars):
        for tpms_id in car.tpms_sensor_ids:
            tpms_to_car_index[tpms_id] = index

    groups: dict[tuple[str, int], list[ObservationResponseDto]] = defaultdict(list)

    for observation in observations:
        car_index = tpms_to_car_index.get(observation.tpms_sensor_id)
        if car_index is None:
            continue
        key = (observation.observation_sensor_id, car_index)
        groups[key].append(observation)

    result: list[CreateCarObservationDto] = []

    for (observation_sensor_id, car_index), observation_group in groups.items():
        observation_group.sort(key=lambda o: o.timestamp)

        clusters: list[list[ObservationResponseDto]] = []
        current_cluster: list[ObservationResponseDto] = [observation_group[0]]

        for i in range(1, len(observation_group)):
            prev = observation_group[i - 1]
            curr = observation_group[i]
            time_difference = (curr.timestamp - prev.timestamp).total_seconds()

            if time_difference <= 90:
                current_cluster.append(curr)
            else:
                clusters.append(current_cluster)
                current_cluster = [curr]

        clusters.append(current_cluster)

        for cluster in clusters:
            result.append(
                CreateCarObservationDto(
                    timestamp=cluster[0].timestamp,
                    car_id=car_index,
                    observation_ids=[o.id for o in cluster],
                    observation_sensor_id=observation_sensor_id,
                )
            )
    return result


def normalize_affinity_matrix(
    affinity_matrix: NDArray[np.float64],
) -> NDArray[np.float64]:
    if affinity_matrix.size == 0:
        return affinity_matrix
    max_value = affinity_matrix.max()
    if max_value == 0:
        return affinity_matrix
    return affinity_matrix / max_value


def validate_clustering_matrix(matrix: NDArray[np.float64]) -> None:
    if matrix.ndim != 2:
        raise ValueError(
            f"clustering matrix must be 2-dimensional, got {matrix.ndim} dimensions"
        )
    rows, cols = matrix.shape
    if rows != cols:
        raise ValueError(
            f"clustering matrix must be square, got shape ({rows}, {cols})"
        )
    if rows == 0:
        return
    diagonal = np.diagonal(matrix)
    if not np.all(diagonal == 0):
        raise ValueError(
            f"clustering matrix must have zeros on the diagonal, got {diagonal.tolist()}"
        )
