import type {
  CreateObservationSensorDto,
  ObservationSensorResponseDto,
} from "../../types/observationSensorTypes";
import { api } from "../api";

export async function fetchObservationSensors(): Promise<
  ObservationSensorResponseDto[]
> {
  const { data } = await api.get<ObservationSensorResponseDto[]>(
    "/observation_sensors",
  );
  return data;
}

export async function createObservationSensor(
  payload: CreateObservationSensorDto,
): Promise<ObservationSensorResponseDto> {
  const { data } = await api.post<ObservationSensorResponseDto>(
    "/observation_sensors",
    payload,
  );
  return data;
}
