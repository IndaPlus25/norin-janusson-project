import { useQueries, useQuery } from "@tanstack/react-query";

import { carObservationKeys } from "./carObservation.keys";
import {
  fetchCarObservation,
  fetchRecentCarObservationsForGeneration,
} from "./carObservation.api";

export function useRecentCarObservationsForGenerations(
  generationIds: number[],
  maxAgeMs: number,
) {
  return useQueries({
    queries: generationIds.map((generationId) => ({
      queryKey: carObservationKeys.list({ generationId, maxAgeMs }),
      queryFn: () =>
        fetchRecentCarObservationsForGeneration(generationId, maxAgeMs),
      staleTime: Infinity,
      refetchOnWindowFocus: false,
    })),
  });
}

export function useCarObservation(id: number) {
  return useQuery({
    queryKey: carObservationKeys.detail(id),
    queryFn: () => fetchCarObservation(id),
  });
}
