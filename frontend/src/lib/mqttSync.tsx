import { useEffect, useRef } from "react";
import { useAppStore } from "../stores/appStore";
import { getMqttClient } from "./mqtt";

export function MqttSync() {
  const selectedGenerationIds = useAppStore((s) => s.selectedGenerationIds);
  const mqttStatus = useAppStore((s) => s.mqttStatus);
  const subscribed = useRef<Set<string>>(new Set());

  useEffect(() => {
    if (mqttStatus !== "connected") return;
    const client = getMqttClient();
    if (!client) return;

    const desired = computeTopics(selectedGenerationIds);
    const current = subscribed.current;

    const toSub = [...desired].filter((t) => !current.has(t));
    const toUnsub = [...current].filter((t) => !desired.has(t));

    if (toSub.length) client.subscribe(toSub);
    if (toUnsub.length) client.unsubscribe(toUnsub);

    subscribed.current = desired;
  }, [selectedGenerationIds, mqttStatus]);

  return null;
}

function computeTopics(generationIds: number[]): Set<string> {
  const topics = new Set<string>();
  generationIds.forEach((id) =>
    topics.add(`generation/${id}/car/+/car-observation/+`),
  );
  return topics;
}
