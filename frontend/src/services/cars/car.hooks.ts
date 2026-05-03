import { carKeys } from "./car.keys";
import { fetchCarsForGeneration, renameCar } from "./car.api";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

export function useFetchCarsForGeneration(generationId: number) {
  return useQuery({
    queryKey: carKeys.list({ generationId }),
    queryFn: () => fetchCarsForGeneration(generationId),
  });
}

export function useRenameCar(carId: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: { name: string }) => renameCar(payload, carId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: carKeys.all });
    },
  });
}
