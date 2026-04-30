import type { CarObservationResponseDto } from "../../types/carObservationTypes";
import { api } from "../api";

export async function fetchRecentCarObservationsForGeneration(
  generationId: number,
  maxAgeMs: number,
): Promise<CarObservationResponseDto[]> {
  const { data } = await api.get<CarObservationResponseDto[]>(
    `/generation/${generationId}/timeframe/${maxAgeMs}`,
  );
  return data;
}
export async function fetchCarObservation(
  carObservationId: number,
): Promise<CarObservationResponseDto> {
  const { data } = await api.get<CarObservationResponseDto>(
    `/car_observation/${carObservationId}`,
  );
  return data;
}
