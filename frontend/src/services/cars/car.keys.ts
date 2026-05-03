export const carKeys = {
  all: ["car"] as const,
  lists: () => [...carKeys.all, "list"] as const,
  list: (filters?: Record<string, unknown>) =>
    [...carKeys.lists(), filters ?? {}] as const,
  details: () => [...carKeys.all, "detail"] as const,
  detail: (id: number) => [...carKeys.details(), id] as const,
};
