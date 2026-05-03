import { create } from "zustand";
import { persist } from "zustand/middleware";

export type MqttStatus = "idle" | "connected" | "reconnecting" | "disconnected";

export const DEFAULT_MAX_AGE_MS = 3_600_000;

type AppStore = {
  mqttStatus: MqttStatus;
  selectedGenerationIds: number[];
  selectedCarIds: number[];
  selectedMaxAgeMs: number;

  setMqttStatus: (s: MqttStatus) => void;
  selectGeneration: (generationId: number) => void;
  unselectGeneration: (generationId: number) => void;
  selectCar: (carId: number) => void;
  unselectCar: (carId: number) => void;
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
      selectedCarIds: [],
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
        set((state) => ({
          selectedGenerationIds: removeId(
            state.selectedGenerationIds,
            generationId,
          ),
        })),

      selectCar: (carId) =>
        set((state) => ({
          selectedCarIds: addUnique(state.selectedCarIds, carId),
        })),

      unselectCar: (carId) =>
        set((state) => ({
          selectedCarIds: removeId(state.selectedCarIds, carId),
        })),
    }),
    {
      name: "app-store",
      partialize: (s) => ({
        selectedGenerationIds: s.selectedGenerationIds,
        selectedCarIds: s.selectedCarIds,
        selectedMaxAgeMs: s.selectedMaxAgeMs,
      }),
    },
  ),
);
