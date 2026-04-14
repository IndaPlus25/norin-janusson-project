from data.DTO_objects import TPMSSensorFormatted


def affinity_to_euclidian(affinity_matrix: list[list[float]]):
    return 1 - affinity_matrix


def create_tpms_sensor_dict(
    affinity_matrix: list[TPMSSensorFormatted],
) -> dict[int, TPMSSensorFormatted]:
    return
