from numpy.random import randint, choice

from clustering.clustering_ops import create_generation_data
from data.DTO_objects import (
    CreateGenerationDto,
    CreateObservationDto,
    CreateObservationSensorDto,
    CreateTPMSSensorDto,
)
from datetime import datetime, timedelta
from db.DB_ops import (
    create_generation,
    create_observation_sensor,
    create_TPMS_sensor,
    create_observation,
    get_all_observations,
    get_all_tpms_sensors,
    get_generation,
)


def test_test_aceptable_error_rate():
    create_generation_dto = CreateGenerationDto("test_generation")
    generation_id = create_generation(create_generation_dto)
    generation_response_dto = get_generation(generation_id)

    create_observation_sensor_dto_1 = CreateObservationSensorDto(
        "observation_sensor_1_id",
        "observation_sensor_1_name",
        10.677375,
        -137.829771,
        "gröndalsvägen_1",
    )
    create_observation_sensor_dto_2 = CreateObservationSensorDto(
        "observation_sensor_2_id",
        "observation_sensor_2_name",
        10.677375,
        -137.829771,
        "gröndalsvägen_2",
    )
    create_observation_sensor_dto_3 = CreateObservationSensorDto(
        "observation_sensor_3_id",
        "observation_sensor_3_name",
        10.677375,
        -137.829771,
        "gröndalsvägen_3",
    )
    create_observation_sensor_dto_4 = CreateObservationSensorDto(
        "observation_sensor_4_id",
        "observation_sensor_4_name",
        10.677375,
        -137.829771,
        "gröndalsvägen_4",
    )
    create_observation_sensor_dto_5 = CreateObservationSensorDto(
        "observation_sensor_5_id",
        "observation_sensor_5_name",
        10.677375,
        -137.829771,
        "gröndalsvägen_5",
    )

    observation_sensor_id_1 = create_observation_sensor(create_observation_sensor_dto_1)
    observation_sensor_id_2 = create_observation_sensor(create_observation_sensor_dto_2)
    observation_sensor_id_3 = create_observation_sensor(create_observation_sensor_dto_3)
    observation_sensor_id_4 = create_observation_sensor(create_observation_sensor_dto_4)
    observation_sensor_id_5 = create_observation_sensor(create_observation_sensor_dto_5)

    observation_sensor_ids = [
        observation_sensor_id_1,
        observation_sensor_id_2,
        observation_sensor_id_3,
        observation_sensor_id_4,
        observation_sensor_id_5,
    ]

    tpms_sensor_dict: dict[int, list[str]] = {}

    create_tpms_sensor_dto_1 = CreateTPMSSensorDto("sensor_1_car_1", "type_1")
    create_tpms_sensor_dto_2 = CreateTPMSSensorDto("sensor_2_car_1", "type_1")
    create_tpms_sensor_dto_3 = CreateTPMSSensorDto("sensor_3_car_1", "type_1")
    create_tpms_sensor_dto_4 = CreateTPMSSensorDto("sensor_4_car_1", "type_1")

    tpms_sensopr_id_1 = create_TPMS_sensor(create_tpms_sensor_dto_1)
    tpms_sensopr_id_2 = create_TPMS_sensor(create_tpms_sensor_dto_2)
    tpms_sensopr_id_3 = create_TPMS_sensor(create_tpms_sensor_dto_3)
    tpms_sensopr_id_4 = create_TPMS_sensor(create_tpms_sensor_dto_4)

    tpms_sensor_dict[1] = [
        tpms_sensopr_id_1,
        tpms_sensopr_id_2,
        tpms_sensopr_id_3,
        tpms_sensopr_id_4,
    ]

    create_tpms_sensor_dto_5 = CreateTPMSSensorDto("sensor_5_car_2", "type_2")
    create_tpms_sensor_dto_6 = CreateTPMSSensorDto("sensor_6_car_2", "type_2")
    create_tpms_sensor_dto_7 = CreateTPMSSensorDto("sensor_7_car_2", "type_2")
    create_tpms_sensor_dto_8 = CreateTPMSSensorDto("sensor_8_car_2", "type_2")

    tpms_sensopr_id_5 = create_TPMS_sensor(create_tpms_sensor_dto_5)
    tpms_sensopr_id_6 = create_TPMS_sensor(create_tpms_sensor_dto_6)
    tpms_sensopr_id_7 = create_TPMS_sensor(create_tpms_sensor_dto_7)
    tpms_sensopr_id_8 = create_TPMS_sensor(create_tpms_sensor_dto_8)

    tpms_sensor_dict[2] = [
        tpms_sensopr_id_5,
        tpms_sensopr_id_6,
        tpms_sensopr_id_7,
        tpms_sensopr_id_8,
    ]
    create_tpms_sensor_dto_9 = CreateTPMSSensorDto("sensor_9_car_3", "type_3")
    create_tpms_sensor_dto_10 = CreateTPMSSensorDto("sensor_10_car_3", "type_3")
    create_tpms_sensor_dto_11 = CreateTPMSSensorDto("sensor_11_car_3", "type_3")
    create_tpms_sensor_dto_12 = CreateTPMSSensorDto("sensor_12_car_3", "type_3")

    tpms_sensopr_id_9 = create_TPMS_sensor(create_tpms_sensor_dto_9)
    tpms_sensopr_id_10 = create_TPMS_sensor(create_tpms_sensor_dto_10)
    tpms_sensopr_id_11 = create_TPMS_sensor(create_tpms_sensor_dto_11)
    tpms_sensopr_id_12 = create_TPMS_sensor(create_tpms_sensor_dto_12)

    tpms_sensor_dict[3] = [
        tpms_sensopr_id_9,
        tpms_sensopr_id_10,
        tpms_sensopr_id_11,
        tpms_sensopr_id_12,
    ]
    create_tpms_sensor_dto_13 = CreateTPMSSensorDto("sensor_13_car_4", "type_4")
    create_tpms_sensor_dto_14 = CreateTPMSSensorDto("sensor_14_car_4", "type_4")
    create_tpms_sensor_dto_15 = CreateTPMSSensorDto("sensor_15_car_4", "type_4")
    create_tpms_sensor_dto_16 = CreateTPMSSensorDto("sensor_16_car_4", "type_4")

    tpms_sensopr_id_13 = create_TPMS_sensor(create_tpms_sensor_dto_13)
    tpms_sensopr_id_14 = create_TPMS_sensor(create_tpms_sensor_dto_14)
    tpms_sensopr_id_15 = create_TPMS_sensor(create_tpms_sensor_dto_15)
    tpms_sensopr_id_16 = create_TPMS_sensor(create_tpms_sensor_dto_16)

    tpms_sensor_response_dtos = get_all_tpms_sensors()

    tpms_sensor_dict[4] = [
        tpms_sensopr_id_13,
        tpms_sensopr_id_14,
        tpms_sensopr_id_15,
        tpms_sensopr_id_16,
    ]

    for i in range(1, 5):
        _create_observations_for_car(tpms_sensor_dict, observation_sensor_ids, i)

    observation_response_dtos = get_all_observations()

    create_car_dtos, create_car_observation_dtos = create_generation_data(
        generation_response_dto, tpms_sensor_response_dtos, observation_response_dtos
    )

    tpms_id_to_true_car_id: dict[str, int] = {}
    for true_car_id, tpms_sensor_ids in tpms_sensor_dict.items():
        for tpms_sensor_id in tpms_sensor_ids:
            tpms_id_to_true_car_id[tpms_sensor_id] = true_car_id

    observation_by_id = {}
    for observation in observation_response_dtos:
        observation_by_id[observation.id] = observation

    # Every true tpms sensor is assigned to one guessed car.
    all_true_tpms_ids: list[str] = []
    for tpms_sensor_ids in tpms_sensor_dict.values():
        all_true_tpms_ids.extend(tpms_sensor_ids)

    assigned_tpms_ids: list[str] = []
    for guessed_car in create_car_dtos:
        assigned_tpms_ids.extend(guessed_car.tpms_sensor_ids)

    assert sorted(assigned_tpms_ids) == sorted(all_true_tpms_ids), (
        f"tpms assignment mismatch.\n"
        f"  expected: {sorted(all_true_tpms_ids)}\n"
        f"  got:      {sorted(assigned_tpms_ids)}"
    )

    # Each guessed cluster matches one of the true clusters.
    true_clusters: list[list[str]] = []
    for tpms_sensor_ids in tpms_sensor_dict.values():
        true_clusters.append(sorted(tpms_sensor_ids))
    true_clusters.sort()

    guessed_clusters: list[list[str]] = []
    for guessed_car in create_car_dtos:
        guessed_clusters.append(sorted(guessed_car.tpms_sensor_ids))
    guessed_clusters.sort()

    assert guessed_clusters == true_clusters, (
        f"cluster shape mismatch.\n"
        f"  expected: {true_clusters}\n"
        f"  got:      {guessed_clusters}"
    )

    # Map each guessed-car index to the true car it represents.
    guessed_car_index_to_true_car_id: dict[int, int] = {}
    for guessed_car_index, guessed_car in enumerate(create_car_dtos):
        first_tpms_sensor_id = guessed_car.tpms_sensor_ids[0]
        guessed_car_index_to_true_car_id[guessed_car_index] = tpms_id_to_true_car_id[
            first_tpms_sensor_id
        ]

    # Each car_observation is correct.
    for car_observation_index, car_observation in enumerate(
        create_car_observation_dtos
    ):
        member_observations = []
        for observation_id in car_observation.observation_ids:
            member_observations.append(observation_by_id[observation_id])
        assert (
            member_observations
        ), f"car_observation[{car_observation_index}] has no member observations"

        # Meember observations come from the same true car.
        member_true_car_ids: set[int] = set()
        for member_observation in member_observations:
            member_true_car_ids.add(
                tpms_id_to_true_car_id[member_observation.tpms_sensor_id]
            )
        assert len(member_true_car_ids) == 1, (
            f"car_observation[{car_observation_index}] mixes true cars "
            f"{sorted(member_true_car_ids)}"
        )

        # True car matches the guessed car the car_observation points at.
        member_true_car_id = list(member_true_car_ids)[0]
        guessed_true_car_id = guessed_car_index_to_true_car_id[car_observation.car_id]
        assert member_true_car_id == guessed_true_car_id, (
            f"car_observation[{car_observation_index}] members come from true car "
            f"{member_true_car_id} but its car_index points at a guess for true car "
            f"{guessed_true_car_id}"
        )

        # All member observations share the car_observation's observation_sensor.
        for member_observation in member_observations:
            assert (
                member_observation.observation_sensor_id
                == car_observation.observation_sensor_id
            ), f"car_observation[{car_observation_index}] mixes observation_sensor_ids"

        # Member observations are within the 90 seconds.
        member_timestamps: list[datetime] = []
        for member_observation in member_observations:
            member_timestamps.append(member_observation.timestamp)
        member_timestamps.sort()
        for j in range(1, len(member_timestamps)):
            gap_seconds = (
                member_timestamps[j] - member_timestamps[j - 1]
            ).total_seconds()
            assert (
                gap_seconds <= 90
            ), f"car_observation[{car_observation_index}] has a {gap_seconds:.1f}s gap "

    # Every observation belonging to an assigned tpms ends up in exactly one car_observation, and nothing else does.
    assigned_tpms_id_set = set(assigned_tpms_ids)
    expected_observation_ids: set[int] = set()
    for observation in observation_response_dtos:
        if observation.tpms_sensor_id in assigned_tpms_id_set:
            expected_observation_ids.add(observation.id)

    collected_observation_ids: list[int] = []
    for car_observation in create_car_observation_dtos:
        collected_observation_ids.extend(car_observation.observation_ids)

    assert set(collected_observation_ids) == expected_observation_ids, (
        f"observation coverage mismatch.\n"
        f"  missing:    {expected_observation_ids - set(collected_observation_ids)}\n"
        f"  unexpected: {set(collected_observation_ids) - expected_observation_ids}"
    )
    assert len(collected_observation_ids) == len(
        set(collected_observation_ids)
    ), "an observation appears in more than one car_observation"


def _create_observations_for_car(
    tpms_sensor_dict: dict[int, list[str]],
    observation_sensor_ids: list[str],
    car_temp_id: int,
):
    previous_observation: int = 100
    observation_range = len(observation_sensor_ids)
    for _ in range(9):
        r = randint(0, observation_range - 1)
        if r < previous_observation:
            previous_observation = r
        else:
            previous_observation = r + 1

        _create_observations_for_car_at_point(
            tpms_sensor_dict, observation_sensor_ids[previous_observation], car_temp_id
        )

    return


def _create_observations_for_car_at_point(
    tpms_sensor_dict: dict[int, list[str]], observation_sensor_id: str, car_temp_id: int
):
    observations = _generate_observations_at_point(
        tpms_sensor_dict, observation_sensor_id, car_temp_id
    )
    for observation in observations:
        create_observation(observation)
    return


def _generate_observations_at_point(
    tpms_sensor_dict: dict[int, list[str]],
    observation_sensor_id: str,
    car_temp_id: int,
) -> list[CreateObservationDto]:
    count = randint(0, 6)
    if count == 0:
        return []

    available_tpms = tpms_sensor_dict.get(car_temp_id, [])
    if not available_tpms:
        return []

    observations: list[CreateObservationDto] = []
    last_seen: dict[str, datetime] = {}
    current_time = datetime.now()

    for i in range(count):
        if i > 0:
            current_time += timedelta(seconds=randint(1, 90))

        eligible = [
            tid
            for tid in available_tpms
            if tid not in last_seen
            or (current_time - last_seen[tid]).total_seconds() >= 60
        ]

        if not eligible:
            break

        tpms_id = choice(eligible)
        observations.append(
            CreateObservationDto(
                tpms_sensor_id=tpms_id,
                observation_sensor_id=observation_sensor_id,
                timestamp=current_time,
            )
        )
        last_seen[tpms_id] = current_time

    return observations
