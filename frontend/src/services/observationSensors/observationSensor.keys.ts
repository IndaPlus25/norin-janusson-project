export const observationSensorKeys = {
  all: ["observation_sensors"] as const,
  lists: () => [...observationSensorKeys.all, "list"] as const,
  list: (filters?: Record<string, unknown>) =>
    [...observationSensorKeys.lists(), filters ?? {}] as const,
  details: () => [...observationSensorKeys.all, "detail"] as const,
  detail: (id: string) => [...observationSensorKeys.details(), id] as const,
};
