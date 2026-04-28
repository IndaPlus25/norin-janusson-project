export type CreateObservationDto = {
  tpms_sensor_id: string;
  observation_sensor_id: string;
  timestamp: string;
};

export type ObservationResponseDto = {
  id: number;
  timestamp: string;
  observation_sensor_id: string;
  tpms_sensor_id: string;
  car_observation_ids: number[];
};
