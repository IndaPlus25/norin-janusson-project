import { useEffect } from "react";
import { useAppStore } from "../../../stores/appStore";
import { useRecentCarObservationsForGenerations } from "../../../services/carObservations/carObservation.hooks";
import { pruneStaleObservations } from "../../../services/mqtt";
import CarObservationListItem from "./CarObservationListItem";
import TimeframePicker from "./TimeframePicker";

export default function CarObservationList() {
  const selectedGenerationIds = useAppStore((s) => s.selectedGenerationIds);
  const selectedMaxAgeMs = useAppStore((s) => s.selectedMaxAgeMs);

  useEffect(() => {
    pruneStaleObservations(selectedMaxAgeMs);
  }, [selectedMaxAgeMs]);

  const queries = useRecentCarObservationsForGenerations(
    selectedGenerationIds,
    selectedMaxAgeMs,
  );

  if (selectedGenerationIds.length === 0) {
    return (
      <>
        <TimeframePicker />
        <p>select a generation to view car observations</p>
      </>
    );
  }

  const isLoading = queries.some((q) => q.isLoading);
  const firstError = queries.find((q) => q.error)?.error;

  if (isLoading)
    return (
      <>
        <TimeframePicker />
        <p>loading...</p>
      </>
    );
  if (firstError)
    return (
      <>
        <TimeframePicker />
        <p>error: {firstError.message}</p>
      </>
    );

  const observations = queries
    .flatMap((q) => q.data ?? [])
    .sort((a, b) => b.timestamp.localeCompare(a.timestamp));

  return (
    <>
      <TimeframePicker />
      {observations.length === 0 ? (
        <p>no recent observations</p>
      ) : (
        <ul>
          {observations.map((co) => (
            <CarObservationListItem key={co.id} carObservation={co} />
          ))}
        </ul>
      )}
    </>
  );
}
