from clustering.util_funcs import (
    affinity_to_euclidian,
    create_car_observations,
    get_empty_base_matrix,
    get_observation_dict,
    get_sub_cluster_matrix,
)
from clustering.affinity_matrix_creation import (
    add_observation_coocurence,
    add_sensor_type_coocurence,
)
from clustering.matrix_clustering import apply_HDBSCAN, partition_cluster
from data.DTO_objects import (
    CreateCarDto,
    CreateCarObservationDto,
    GenerationResponseDto,
    ObservationResponseDto,
    TPMSSensorResponseDto,
)


def create_cars_guesses(
    generation: GenerationResponseDto,
    tpms_sensors: list[TPMSSensorResponseDto],
    observations: list[ObservationResponseDto],
) -> tuple[list[CreateCarDto], list[CreateCarObservationDto]]:
    observation_dict = get_observation_dict(observations)
    base_matrix, tpms_sensor_dict = get_empty_base_matrix(tpms_sensors)
    base_matrix = add_observation_coocurence(
        base_matrix, tpms_sensor_dict, observation_dict
    )
    base_matrix = add_sensor_type_coocurence(base_matrix, tpms_sensors)
    euclidian_matrix = affinity_to_euclidian(base_matrix)
    _, clusters, clusters_to_partition = apply_HDBSCAN(euclidian_matrix)
    car_guesses = [
        CreateCarDto(
            None,
            generation.id,
            [tpms_sensor_dict[tpms_sensor_key].id for tpms_sensor_key in cluster],
        )
        for cluster in clusters
    ]
    for cluster in clusters_to_partition:
        sub_cluster_matrix, cluster_map_dict = get_sub_cluster_matrix(
            euclidian_matrix, cluster
        )
        partitioned_clusters = partition_cluster(sub_cluster_matrix)
        new_car_guesses = [
            CreateCarDto(
                None,
                generation.id,
                [
                    tpms_sensor_dict[cluster_map_dict[tpms_sensor_key]].id
                    for tpms_sensor_key in partitioned_cluster
                ],
            )
            for partitioned_cluster in partitioned_clusters
        ]
        car_guesses.extend(new_car_guesses)

    return (car_guesses, create_car_observations(observations, car_guesses))
