import { create } from "zustand";
import { persist } from "zustand/middleware";

export type MqttStatus = "idle" | "connected" | "reconnecting" | "disconnected";

//TODO: maybe just remove? ads complexity and imports but doesnt contribute much to logic i think, check later
type AppStore = {
  mqttStatus: MqttStatus;
  generations: number[];
  selectedCarIds: number[];

  setMqttStatus: (s: MqttStatus) => void;
  addGeneration: (generationId: number) => void;
  removeGeneration: (generationId: number) => void;
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
      generations: [],
      selectedCarIds: [],

      setMqttStatus: (s) => set({ mqttStatus: s }),

      addGeneration: (generationId) =>
        set((state) => ({
          generations: addUnique(state.generations, generationId),
        })),

      removeGeneration: (generationId) =>
        set((state) => ({
          generations: removeId(state.generations, generationId),
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
        generations: s.generations,
        selectedCarIds: s.selectedCarIds,
      }),
    },
  ),
);
