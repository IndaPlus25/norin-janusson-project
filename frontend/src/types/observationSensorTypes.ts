import type { EPSG } from "./enums";

export type CreateObservationSensorDto = {
  id: string;
  name: string;
  lat: number;
  lng: number;
  address: string;
};

export type ObservationSensorResponseDto = {
  id: string;
  name: string;
  lat: number;
  lng: number;
  epsg: EPSG;
  address: string;
  active: boolean;
  observation_ids: number[];
  car_observation_ids: number[];
};
