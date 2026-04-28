export const observationSensorKeys = {
  all: ["observations"] as const,
  lists: () => [...observationSensorKeys.all, "list"] as const,
  list: (filters?: Record<string, unknown>) =>
    [...observationSensorKeys.lists(), filters ?? {}] as const,
  details: () => [...observationSensorKeys.all, "detail"] as const,
  detail: (id: number) => [...observationSensorKeys.details(), id] as const,
};
