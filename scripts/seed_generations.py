"""
Replays the synthetic dataset from tests/clustering/test_clustering_ops.py
through MQTT so the running backend ingests it the same way real hardware
would.

Prerequisites:
  - mosquitto + redis up (`docker-compose up`)
  - backend running (subscribed to topic "tpms")
  - the 5 observation sensors below already created (via the GUI form)

Run:
  python3 code/scripts/seed_observations.py
  python3 code/scripts/seed_observations.py --cars 2 --passes 5
"""

import argparse
import json
import random
from datetime import datetime, timedelta, timezone

import paho.mqtt.publish as publish

HOST = "localhost"
PORT = 1883
TOPIC = "tpms"

OBSERVATION_SENSOR_IDS = [
    "observation_sensor_1_id",
    "observation_sensor_2_id",
    "observation_sensor_3_id",
    "observation_sensor_4_id",
    "observation_sensor_5_id",
]

# Mirrors the (car -> [4 tpms ids]) layout used by test_clustering_ops.py.
CARS = {
    1: (
        "type_1",
        ["sensor_1_car_1", "sensor_2_car_1", "sensor_3_car_1", "sensor_4_car_1"],
    ),
    2: (
        "type_2",
        ["sensor_5_car_2", "sensor_6_car_2", "sensor_7_car_2", "sensor_8_car_2"],
    ),
    3: (
        "type_3",
        ["sensor_9_car_3", "sensor_10_car_3", "sensor_11_car_3", "sensor_12_car_3"],
    ),
    4: (
        "type_4",
        ["sensor_13_car_4", "sensor_14_car_4", "sensor_15_car_4", "sensor_16_car_4"],
    ),
}


def publish_observation(
    observation_sensor_id: str, tpms_id: str, sensor_type: str, ts: datetime
) -> None:
    payload = {
        "observation_sensor_id": observation_sensor_id,
        "id": tpms_id,
        "type": sensor_type,
        "time": ts.isoformat(),
    }
    publish.single(TOPIC, json.dumps(payload), hostname=HOST, port=PORT)


def generate_observations_at_point(
    tpms_ids: list[str], sensor_type: str, observation_sensor_id: str, start: datetime
) -> list[tuple[str, str, str, datetime]]:
    count = random.randint(0, 5)
    if count == 0:
        return []

    out: list[tuple[str, str, str, datetime]] = []
    last_seen: dict[str, datetime] = {}
    current_time = start

    for i in range(count):
        if i > 0:
            current_time += timedelta(seconds=random.randint(1, 89))

        eligible = [
            tid
            for tid in tpms_ids
            if tid not in last_seen
            or (current_time - last_seen[tid]).total_seconds() >= 60
        ]
        if not eligible:
            break

        tpms_id = random.choice(eligible)
        out.append((observation_sensor_id, tpms_id, sensor_type, current_time))
        last_seen[tpms_id] = current_time

    return out


def generate_observations_for_car(
    tpms_ids: list[str], sensor_type: str, passes: int, start: datetime
) -> list[tuple[str, str, str, datetime]]:
    sensor_count = len(OBSERVATION_SENSOR_IDS)
    previous_index = 100  # sentinel >= sensor_count, matches the test's trick
    point_time = start
    out: list[tuple[str, str, str, datetime]] = []

    for _ in range(passes):
        r = random.randint(0, sensor_count - 2)  # numpy.randint(0, n-1) → [0, n-2]
        if r < previous_index:
            previous_index = r
        else:
            previous_index = r + 1

        observation_sensor_id = OBSERVATION_SENSOR_IDS[previous_index]
        out.extend(
            generate_observations_at_point(
                tpms_ids, sensor_type, observation_sensor_id, point_time
            )
        )
        # Advance the per-pass clock so points don't overlap across passes.
        point_time += timedelta(seconds=120)

    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cars", type=int, default=len(CARS), help="Number of cars (1..4)"
    )
    parser.add_argument(
        "--passes",
        type=int,
        default=9,
        help="Sensor points per car (matches test default of 9)",
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Optional RNG seed for reproducibility"
    )
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    car_ids = list(CARS.keys())[: args.cars]
    base_start = datetime.now(timezone.utc)

    # Stagger car timelines so two cars never appear at the same observation
    # sensor within the 60s window that drives co-occurrence — otherwise
    # HDBSCAN sees uniform affinity and labels everything as noise.
    # Worst-case car session: passes * 120s point gap + 6 obs * 89s drift.
    car_session_seconds = args.passes * 120 + 6 * 89 + 60

    all_messages: list[tuple[str, str, str, datetime]] = []

    for i, car_id in enumerate(car_ids):
        sensor_type, tpms_ids = CARS[car_id]
        car_start = base_start + timedelta(seconds=i * car_session_seconds)
        all_messages.extend(
            generate_observations_for_car(tpms_ids, sensor_type, args.passes, car_start)
        )

    # Send in chronological order so the receiver sees them as if real-time.
    all_messages.sort(key=lambda m: m[3])

    print(f"publishing {len(all_messages)} observations to {HOST}:{PORT}/{TOPIC}")
    for i, (observation_sensor_id, tpms_id, sensor_type, ts) in enumerate(
        all_messages, 1
    ):
        publish_observation(observation_sensor_id, tpms_id, sensor_type, ts)
        if i % 10 == 0:
            print(f"  sent {i}/{len(all_messages)}")
    print("done")


if __name__ == "__main__":
    main()
