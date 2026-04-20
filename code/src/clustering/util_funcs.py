from data.DTO_objects import ObservationResponseDto, TPMSSensorResponseDto


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
