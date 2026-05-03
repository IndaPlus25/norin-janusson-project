export const generationKeys = {
  all: ["generation"] as const,
  lists: () => [...generationKeys.all, "list"] as const,
  list: (filters?: Record<string, unknown>) =>
    [...generationKeys.lists(), filters ?? {}] as const,
  details: () => [...generationKeys.all, "detail"] as const,
  detail: (id: number) => [...generationKeys.details(), id] as const,
};
