import { create } from "zustand";
import { persist } from "zustand/middleware";

export type MqttStatus = "idle" | "connected" | "reconnecting" | "disconnected";

export const DEFAULT_MAX_AGE_MS = 3_600_000;

type AppStore = {
  mqttStatus: MqttStatus;
  selectedGenerationIds: number[];
  selectedCarIdsByGeneration: Record<number, number[]>;
  selectedMaxAgeMs: number;

  setMqttStatus: (s: MqttStatus) => void;
  selectGeneration: (generationId: number) => void;
  unselectGeneration: (generationId: number) => void;
  selectCar: (generationId: number, carId: number) => void;
  unselectCar: (generationId: number, carId: number) => void;
  setSelectedMaxAgeMs: (ms: number) => void;
};

function addUnique(list: number[], id: number): number[] {
  return list.includes(id) ? list : [...list, id];
}

function removeId(list: number[], id: number): number[] {
  return list.filter((x) => x !== id);
}

export const useAppStore = create<AppStore>()(
  persist(
    (set) => ({
      mqttStatus: "idle",
      selectedGenerationIds: [],
      selectedCarIdsByGeneration: {},
      selectedMaxAgeMs: DEFAULT_MAX_AGE_MS,

      setMqttStatus: (s) => set({ mqttStatus: s }),
      setSelectedMaxAgeMs: (ms) => set({ selectedMaxAgeMs: ms }),

      selectGeneration: (generationId) =>
        set((state) => ({
          selectedGenerationIds: addUnique(
            state.selectedGenerationIds,
            generationId,
          ),
        })),

      unselectGeneration: (generationId) =>
        set((state) => {
          const { [generationId]: _dropped, ...rest } =
            state.selectedCarIdsByGeneration;
          return {
            selectedGenerationIds: removeId(
              state.selectedGenerationIds,
              generationId,
            ),
            selectedCarIdsByGeneration: rest,
          };
        }),

      selectCar: (generationId, carId) =>
        set((state) => ({
          selectedCarIdsByGeneration: {
            ...state.selectedCarIdsByGeneration,
            [generationId]: addUnique(
              state.selectedCarIdsByGeneration[generationId] ?? [],
              carId,
            ),
          },
        })),

      unselectCar: (generationId, carId) =>
        set((state) => ({
          selectedCarIdsByGeneration: {
            ...state.selectedCarIdsByGeneration,
            [generationId]: removeId(
              state.selectedCarIdsByGeneration[generationId] ?? [],
              carId,
            ),
          },
        })),
    }),
    {
      name: "app-store",
      partialize: (s) => ({
        selectedGenerationIds: s.selectedGenerationIds,
        selectedCarIdsByGeneration: s.selectedCarIdsByGeneration,
        selectedMaxAgeMs: s.selectedMaxAgeMs,
      }),
    },
  ),
);
