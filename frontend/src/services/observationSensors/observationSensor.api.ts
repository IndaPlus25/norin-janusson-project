import type {
  CreateObservationSensorDto,
  ObservationSensorResponseDto,
} from "../../types/observationSensorTypes";
import { api } from "../api";

export async function fetchObservationSensors(): Promise<
  ObservationSensorResponseDto[]
> {
  const { data } = await api.get<ObservationSensorResponseDto[]>(
    "/observation_sensor",
  );
  return data;
}

export async function createObservationSensor(
  payload: CreateObservationSensorDto,
): Promise<ObservationSensorResponseDto> {
  const { data } = await api.post<ObservationSensorResponseDto>(
    "/observation_sensor",
    payload,
  );
  return data;
}
