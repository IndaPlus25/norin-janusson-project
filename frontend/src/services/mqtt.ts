import mqtt, { type MqttClient } from "mqtt";
import { useAppStore } from "../stores/appStore";
import type { CarObservationResponseDto } from "../types/carObservationTypes";
import { queryClient } from "./queryClient";
import { carObservationKeys } from "./carObservations/carObservation.keys";
import type { ObservationSensorResponseDto } from "../types/observationSensorTypes";
import { observationSensorKeys } from "./observationSensors/observationSensor.keys";

const PRUNE_INTERVAL_MS = 60_000;

let client: MqttClient | null = null;
let pruneTimer: ReturnType<typeof setInterval> | null = null;

export function connectMqtt() {
  if (client) return client;

  const url = import.meta.env.VITE_MQTT_URL ?? "ws://localhost:9001";
  client = mqtt.connect(url, {
    clientId: `web-${randomClientId()}`,
    reconnectPeriod: 2000,
  });

  client.on("connect", () => {
    useAppStore.getState().setMqttStatus("connected");
    startPruner();
    client?.subscribe([
      "observation-sensor/+/observation/created",
      "observation-sensor/+/car-observation/created",
    ]);
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
  const data = parsePayload(topic, payload);
  if (data === null) return;

  if (topic.startsWith("observation-sensor/")) {
    handleObservationSensorTopic(topic, data);
  } else if (topic.startsWith("generation/")) {
    handleGenerationTopic(topic, data);
  }
}

function parsePayload(topic: string, payload: Buffer): unknown {
  try {
    return JSON.parse(payload.toString());
  } catch {
    console.warn("non-JSON MQTT payload", topic);
    return null;
  }
}

function handleObservationSensorTopic(topic: string, data: unknown) {
  const [, sensorId, kind] = topic.split("/");

  if (kind === "observation") {
    const { observation_id } = data as { observation_id: number };
    addObservationToObservationSensor(sensorId, observation_id);
  } else if (kind === "car-observation") {
    const { car_observation_id } = data as { car_observation_id: number };
    addCarObservationToObservationSensor(sensorId, car_observation_id);
  }
}

function handleGenerationTopic(topic: string, data: unknown) {
  const event = topic.split("/").at(-1);

  if (event === "created") {
    appendToWindow(data as CarObservationResponseDto);
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

//TODO: check ways to lessen code duplication here, VERY UGLY
function addObservationToObservationSensor(
  observationSensorId: string,
  observationId: number,
) {
  queryClient.setQueriesData<ObservationSensorResponseDto[]>(
    { queryKey: observationSensorKeys.lists() },
    (current) =>
      current?.map((o) => {
        if (o.id !== observationSensorId) return o;
        return {
          ...o,
          observation_ids: [...o.observation_ids, observationId],
        };
      }),
  );
}
function addCarObservationToObservationSensor(
  observationSensorId: string,
  carObservationId: number,
) {
  queryClient.setQueriesData<ObservationSensorResponseDto[]>(
    { queryKey: observationSensorKeys.lists() },
    (current) =>
      current?.map((o) => {
        if (o.id !== observationSensorId) return o;
        return {
          ...o,
          car_observation_ids: [...o.car_observation_ids, carObservationId],
        };
      }),
  );
}
export function pruneStaleObservations(maxAgeMs?: number) {
  const ageMs = maxAgeMs ?? useAppStore.getState().selectedMaxAgeMs;
  const cutoff = Date.now() - ageMs;
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

function randomClientId(): string {
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}
