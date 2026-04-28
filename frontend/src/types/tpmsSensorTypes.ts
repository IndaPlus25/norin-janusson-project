export type CreateTPMSSensorDto = {
  id: string;
  sensor_type: string;
};

export type TPMSSensorResponseDto = {
  id: string;
  sensor_type: string;
  observation_ids: number[];
  car_ids: number[];
};
