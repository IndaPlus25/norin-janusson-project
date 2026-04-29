import { useEffect, useRef } from "react";
import { useAppStore } from "../stores/appStore";
import { getMqttClient } from "./mqtt";

export function MqttSync() {
  const generations = useAppStore((s) => s.generations);
  const subscribed = useRef<Set<string>>(new Set());

  useEffect(() => {
    const client = getMqttClient();
    if (!client) return;

    const desired = computeTopics(generations);
    const current = subscribed.current;

    const toSub = [...desired].filter((t) => !current.has(t));
    const toUnsub = [...current].filter((t) => !desired.has(t));

    if (toSub.length) client.subscribe(toSub);
    if (toUnsub.length) client.unsubscribe(toUnsub);

    subscribed.current = desired;
  }, [generations]);

  return null;
}
function computeTopics(generations: number[]): Set<string> {
  const topics = new Set<string>();
  generations.forEach((gen) =>
    topics.add(`generation/${gen}/car/+/car-observation/+`),
  );
  return topics;
}
