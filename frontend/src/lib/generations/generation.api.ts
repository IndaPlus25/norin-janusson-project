import type {
  CreateGenerationDto,
  GenerationResponseDto,
} from "../../types/generationTypes";
import { api } from "../api";

export async function createGeneration(
  createGenerationDto: CreateGenerationDto,
): Promise<GenerationResponseDto> {
  const { data } = await api.post<GenerationResponseDto>(
    "/generation",
    createGenerationDto,
  );
  return data;
}

export async function fetchGenerations(): Promise<GenerationResponseDto[]> {
  const { data } = await api.get<GenerationResponseDto[]>("/generation");
  return data;
}
