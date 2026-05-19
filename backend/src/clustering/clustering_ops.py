from clustering.util_funcs import (
    affinity_to_euclidian,
    create_car_observations,
    get_empty_base_matrix,
    get_sub_cluster_matrix,
    normalize_affinity_matrix,
    validate_clustering_matrix,
)
from clustering.affinity_matrix_creation import (
    add_observation_coocurence,
    add_sensor_type_coocurence,
)
from clustering.matrix_clustering import (
    apply_HDBSCAN,
    get_best_cluster_size,
    partition_cluster,
)
from clustering.types import ClusteredCar, ClusteringResult
from data.dtos import (
    ObservationResponseDto,
    TPMSSensorResponseDto,
)


def create_generation_data(
    tpms_sensors: list[TPMSSensorResponseDto],
    observations: list[ObservationResponseDto],
) -> ClusteringResult:
    if not tpms_sensors or not observations:
        return ClusteringResult(cars=[], car_observations=[])

    base_matrix, tpms_sensor_dict = get_empty_base_matrix(tpms_sensors)
    base_matrix = add_observation_coocurence(
        base_matrix, tpms_sensor_dict, observations
    )
    base_matrix = add_sensor_type_coocurence(base_matrix, tpms_sensors)
    base_matrix = normalize_affinity_matrix(base_matrix)
    validate_clustering_matrix(base_matrix)
    euclidian_matrix = affinity_to_euclidian(base_matrix)
    _, clusters, clusters_to_partition = apply_HDBSCAN(euclidian_matrix)
    cars: list[ClusteredCar] = [
        ClusteredCar(
            tpms_sensor_ids=[
                tpms_sensor_dict[tpms_sensor_key].id for tpms_sensor_key in cluster
            ]
        )
        for cluster in clusters
    ]
    for cluster in clusters_to_partition:
        sub_cluster_matrix, cluster_map_dict = get_sub_cluster_matrix(
            base_matrix, cluster
        )
        validate_clustering_matrix(sub_cluster_matrix)
        # NOTE: This can result in cluster with more than four values, i.e cars with more than four tpms sensors. Depending on performance we might need a different clustering stategy than spectral.
        sub_cluster_size = len(sub_cluster_matrix)
        min_size = sub_cluster_size // 4
        max_size = sub_cluster_size
        best_cluster_size: int = get_best_cluster_size(
            sub_cluster_matrix, min_size, max_size
        )
        partitioned_clusters, _ = partition_cluster(
            sub_cluster_matrix, best_cluster_size
        )
        cars.extend(
            ClusteredCar(
                tpms_sensor_ids=[
                    tpms_sensor_dict[cluster_map_dict[tpms_sensor_key]].id
                    for tpms_sensor_key in partitioned_cluster
                ]
            )
            for partitioned_cluster in partitioned_clusters
        )

    car_observations = create_car_observations(observations, cars)
    return ClusteringResult(cars=cars, car_observations=car_observations)
