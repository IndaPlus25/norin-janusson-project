import { QueryClient } from "@tanstack/react-query";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30000,
      gcTime: 300000,
      refetchOnWindowFocus: false,
      refetchOnReconnect: false,
      retry: 2,
    },
  },
});
