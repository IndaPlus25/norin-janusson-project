export type CarObservationResponseDto = {
  id: number;
  timestamp: string;
  car_id: number;
  observation_ids: number[];
  observation_sensor_id: string;
};
