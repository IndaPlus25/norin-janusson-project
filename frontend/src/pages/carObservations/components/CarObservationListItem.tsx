import type { CarObservationResponseDto } from "../../../types/carObservationTypes";

type Props = {
  carObservation: CarObservationResponseDto;
};

export default function CarObservationListItem({ carObservation }: Props) {
  return (
    <li>
      <p>id: {carObservation.id}</p>
      <p>timestamp: {carObservation.timestamp}</p>
      <p>car_id: {carObservation.car_id}</p>
      {carObservation.observation_ids.map((observation_id) => (
        <li key={observation_id}>
          <p>observationId: {observation_id}</p>
        </li>
      ))}
      <p>observation_sensor_id: {carObservation.observation_sensor_id}</p>
    </li>
  );
}
