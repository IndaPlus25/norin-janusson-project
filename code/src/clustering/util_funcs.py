from collections import defaultdict

from data.DTO_objects import (
    CreateCarDto,
    CreateCarObservationDto,
    ObservationResponseDto,
    TPMSSensorResponseDto,
)
from numpy import array


def affinity_to_euclidian(affinity_matrix: list[list[float]]) -> list[list[float]]:
    return (1 - array(affinity_matrix)).tolist()


def get_empty_base_matrix(
    tpms_sensors: list[TPMSSensorResponseDto],
) -> tuple[list[list[float]], dict[int, TPMSSensorResponseDto]]:
    tpms_sensor_dict: dict[int, TPMSSensorResponseDto] = {}
    for i, tpms_sensor in enumerate(tpms_sensors):
        tpms_sensor_dict[i] = tpms_sensor
    matrix_size = len(tpms_sensors)
    base_matrix: list[list[float]] = [
        [0.0 for _ in range(matrix_size)] for _ in range(matrix_size)
    ]
    return (base_matrix, tpms_sensor_dict)


def get_observation_dict(
    observations: list[ObservationResponseDto],
) -> dict[int, ObservationResponseDto]:
    observation_dict: dict[int, ObservationResponseDto] = {}
    for observation in observations:
        observation_dict[observation.id] = observation
    return observation_dict


def get_sub_cluster_matrix(
    affinity_matrix: list[list[float]], sub_cluster: list[int]
) -> tuple[list[list[float]], dict[int, int]]:
    cluster_map_dict: dict[int, ObservationResponseDto] = {}
    for sub_cluster_pos, cluster_pos in enumerate(sub_cluster):
        cluster_map_dict[sub_cluster_pos] = cluster_pos

    sub_cluster_matrix_size = len(sub_cluster)
    sub_cluster_matrix: list[list[float]] = [
        [
            affinity_matrix[cluster_map_dict[i]][cluster_map_dict[j]]
            for j in range(sub_cluster_matrix_size)
        ]
        for i in range(sub_cluster_matrix_size)
    ]

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

        car = cars[car_index]
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


def normalize_affinity_matrix(affinity_matrix: list[list[float]]) -> list[list[float]]:
    arr = array(affinity_matrix)
    affinity_matrix = (arr / arr.max()).tolist()
    return affinity_matrix
