import type { ObservationSensorResponseDto } from "../../../types/observationSensorTypes";

type Props = {
  sensor: ObservationSensorResponseDto;
};

export default function ObservationSensorListItem({ sensor }: Props) {
  return (
    <li>
      <p>id: {sensor.id}</p>
      <p>name: {sensor.name}</p>
      <p>
        lat: {sensor.lat}, lng: {sensor.lng}
      </p>
      <p>epsg: {sensor.epsg}</p>
      <p>address: {sensor.address}</p>
      <p>active: {String(sensor.active)}</p>
      <p>observation_ids: {sensor.observation_ids.join(", ") || "(none)"}</p>
      <p>
        car_observation_ids: {sensor.car_observation_ids.join(", ") || "(none)"}
      </p>
    </li>
  );
}
