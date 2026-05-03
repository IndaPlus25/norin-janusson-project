import type { CarResponseDto } from "../../types/carTypes";
import { api } from "../api";

export async function fetchCarsForGeneration(
  generationId: number,
): Promise<CarResponseDto[]> {
  const { data } = await api.get<CarResponseDto[]>(
    `/generation/${generationId}/car`,
  );
  return data;
}

export async function renameCar(
  renameCarPayload: { name: string },
  carId: number,
): Promise<CarResponseDto> {
  const { data } = await api.patch<CarResponseDto>(
    `/car/${carId}/name`,
    renameCarPayload,
  );
  return data;
}
