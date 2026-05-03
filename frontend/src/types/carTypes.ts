export type CarResponseDto = {
  id: number;
  name: string;
  generation_id: number;
  tpms_sensor_ids: string[];
  car_observation_ids: number[];
};
