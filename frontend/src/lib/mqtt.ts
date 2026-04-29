import mqtt, { type MqttClient } from "mqtt";
import { useAppStore } from "../stores/appStore";
import type { CarObservationResponseDto } from "../types/carObservationTypes";
import { queryClient } from "./queryClient";
import { carObservationKeys } from "./carObservations/carObservation.keys";

export const MAX_AGE_MS = 6000000;
const PRUNE_INTERVAL_MS = 60_000;

let client: MqttClient | null = null;
let pruneTimer: ReturnType<typeof setInterval> | null = null;

export function connectMqtt() {
  if (client) return client;

  const url = import.meta.env.VITE_MQTT_URL ?? "ws://localhost:9001";
  client = mqtt.connect(url, {
    clientId: `web-${crypto.randomUUID()}`,
    reconnectPeriod: 2000,
  });

  client.on("connect", () => {
    useAppStore.getState().setMqttStatus("connected");
    startPruner();
  });

  client.on("reconnect", () =>
    useAppStore.getState().setMqttStatus("reconnecting"),
  );
  client.on("close", () =>
    useAppStore.getState().setMqttStatus("disconnected"),
  );
  client.on("error", (err) => console.error("mqtt error", err));

  client.on("message", handleMessage);
  return client;
}

export function getMqttClient() {
  return client;
}

export function disconnectMqtt() {
  stopPruner();
  client?.end();
  client = null;
}

function handleMessage(topic: string, payload: Buffer) {
  const parts = topic.split("/");
  const event = parts.at(-1);

  let data: unknown;
  try {
    data = JSON.parse(payload.toString());
  } catch {
    console.warn("non-JSON MQTT payload", topic);
    return;
  }

  if (event === "created") {
    const obs = data as CarObservationResponseDto;
    appendToWindow(obs);
  } else if (event === "updated") {
    const { car_observation_id, observation_id } = data as {
      car_observation_id: number;
      observation_id: number;
    };
    mergeObservationIntoWindow(car_observation_id, observation_id);
  }
}

function appendToWindow(obs: CarObservationResponseDto) {
  queryClient.setQueriesData<CarObservationResponseDto[]>(
    { queryKey: carObservationKeys.lists() },
    (current) => (current ? [obs, ...current] : [obs]),
  );
}

function mergeObservationIntoWindow(
  carObservationId: number,
  observationId: number,
) {
  queryClient.setQueriesData<CarObservationResponseDto[]>(
    { queryKey: carObservationKeys.lists() },
    (current) =>
      current?.map((o) => {
        if (o.id !== carObservationId) return o;
        return {
          ...o,
          observation_ids: [...o.observation_ids, observationId],
        };
      }),
  );
}

function pruneStaleObservations() {
  const cutoff = Date.now() - MAX_AGE_MS;
  queryClient.setQueriesData<CarObservationResponseDto[]>(
    { queryKey: carObservationKeys.lists() },
    (current) => {
      if (!current) return current;
      const fresh = current.filter(
        (o) => new Date(o.timestamp).getTime() > cutoff,
      );
      return fresh.length === current.length ? current : fresh;
    },
  );
}

function startPruner() {
  if (pruneTimer) return;
  pruneTimer = setInterval(pruneStaleObservations, PRUNE_INTERVAL_MS);
}

function stopPruner() {
  if (pruneTimer) {
    clearInterval(pruneTimer);
    pruneTimer = null;
  }
}
