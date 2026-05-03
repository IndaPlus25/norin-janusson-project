export const carObservationKeys = {
  all: ["car_observation"] as const,
  lists: () => [...carObservationKeys.all, "list"] as const,
  list: (filters?: Record<string, unknown>) =>
    [...carObservationKeys.lists(), filters ?? {}] as const,
  details: () => [...carObservationKeys.all, "detail"] as const,
  detail: (id: number) => [...carObservationKeys.details(), id] as const,
};
