export type CreateGenerationDto = {
  created_at: string;
  name: string;
};

export type GenerationResponseDto = {
  id: number;
  created_at: string;
  name: string;
  car_ids: number[];
};
