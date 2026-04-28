import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { observationSensorKeys } from "./observationSensor.keys";
import {
  createObservationSensor,
  fetchObservationSensors,
} from "./observationSensor.api";
import type { CreateObservationSensorDto } from "../../types/observationSensorTypes";

export function useFetchObservationSensors() {
  return useQuery({
    queryKey: observationSensorKeys.list(),
    queryFn: fetchObservationSensors,
  });
}

export function useCreateObservationSensors() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: CreateObservationSensorDto) =>
      createObservationSensor(payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: observationSensorKeys.lists() });
    },
  });
}
