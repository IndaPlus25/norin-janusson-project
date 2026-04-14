from data.DTO_objects import TPMSSensorFormatted
from datetime import datetime


def add_observation_coocurence(
    base_matrix: list[list[int]], tpms_sensor_dict: dict[int, TPMSSensorFormatted]
) -> list[list[int]]:
    sensor_count = len(tpms_sensor_dict)
    for i in range(0, sensor_count):
        sensor = tpms_sensor_dict.get(i)
        if sensor is None:
            raise ValueError(
                f"Can't get tpms sensor since key {i} does not exist in tpms sensor dictionary"
            )

        for key in sensor.observations.keys():
            for i2 in range(0, sensor_count):
                sensor_to_match = tpms_sensor_dict.get(i2)
                if sensor is None:
                    raise ValueError(
                        f"Can't get match count since key {i2} does not exist in tpms sensor dictionary"
                    )
                matches = count_matches(
                    sensor_to_match.observations[key], sensor.observations[key]
                )
                base_matrix[i][i2] = base_matrix[i][i2] + matches
                base_matrix[i2][i] = base_matrix[i][i2]
    return base_matrix


# TODO: implement
def add_sensor_type_coocurence(
    base_matrix: list[list[int]], sensors: list[TPMSSensorFormatted]
) -> list[list[int]]:
    return


def count_matches(arr1: list[datetime], arr2: list[datetime]) -> int:
    count = 0
    for dt1 in arr1:
        for dt2 in arr2:
            if abs((dt1 - dt2).total_seconds()) <= 60:
                count += 1
    return count
