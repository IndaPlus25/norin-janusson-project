import { create } from "zustand";
import { persist } from "zustand/middleware";

export type MqttStatus = "idle" | "connected" | "reconnecting" | "disconnected";
type AppStore = {
  mqttStatus: MqttStatus;
  selectedGenerationIds: number[];
  selectedCarIds: number[];

  setMqttStatus: (s: MqttStatus) => void;
  selectGeneration: (generationId: number) => void;
  unselectGeneration: (generationId: number) => void;
  selectCar: (carId: number) => void;
  unselectCar: (carId: number) => void;
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

      setMqttStatus: (s) => set({ mqttStatus: s }),

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
      }),
    },
  ),
);
