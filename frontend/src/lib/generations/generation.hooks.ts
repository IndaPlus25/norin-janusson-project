import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import type { CreateGenerationDto } from "../../types/generationTypes";
import { generationKeys } from "./generation.keys";
import { createGeneration, fetchGenerations } from "./generation.api";

export function useFetchGenerations() {
  return useQuery({
    queryKey: generationKeys.list(),
    queryFn: fetchGenerations,
  });
}

export function useCreateGeneration() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: CreateGenerationDto) => createGeneration(payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: generationKeys.all });
    },
  });
}
