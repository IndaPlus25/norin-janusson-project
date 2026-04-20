from data.DTO_objects import (
    CreateCarDto,
    CreateCarObservationDto,
    ObservationResponseDto,
    TPMSSensorResponseDto,
)


def affinity_to_euclidian(affinity_matrix: list[list[float]]) -> list[list[float]]:
    return 1 - affinity_matrix


# TODO:implement
def get_empty_base_matrix(
    tpms_sensors: list[TPMSSensorResponseDto],
) -> tuple[list[list[float]], dict[int, TPMSSensorResponseDto]]:
    return


# TODO:implement
def get_observation_dict(
    observations: list[ObservationResponseDto],
) -> dict[int, ObservationResponseDto]:
    return


# TODO:implement
def get_sub_cluster_matrix(
    euclidian_matrix: list[list[float]], sub_cluster: list[int]
) -> tuple[list[list[float]], dict[int, int]]:
    return


# TODO:implement
def create_car_observations(
    observations: list[ObservationResponseDto], cars: list[CreateCarDto]
) -> list[CreateCarObservationDto]:
    return
