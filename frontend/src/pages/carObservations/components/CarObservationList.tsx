import { useAppStore } from "../../../stores/appStore";
import { useRecentCarObservationsForGenerations } from "../../../lib/carObservations/carObservation.hooks";
import { MAX_AGE_MS } from "../../../lib/mqtt";
import CarObservationListItem from "./CarObservationListItem";

export default function CarObservationList() {
  const selectedGenerationIds = useAppStore((s) => s.selectedGenerationIds);

  const queries = useRecentCarObservationsForGenerations(
    selectedGenerationIds,
    MAX_AGE_MS,
  );

  if (selectedGenerationIds.length === 0) {
    return <p>select a generation to view car observations</p>;
  }

  const isLoading = queries.some((q) => q.isLoading);
  const firstError = queries.find((q) => q.error)?.error;

  if (isLoading) return <p>loading...</p>;
  if (firstError) return <p>error: {firstError.message}</p>;

  const observations = queries
    .flatMap((q) => q.data ?? [])
    .sort((a, b) => b.timestamp.localeCompare(a.timestamp));

  if (observations.length === 0) return <p>no recent observations</p>;

  return (
    <ul>
      {observations.map((co) => (
        <CarObservationListItem key={co.id} carObservation={co} />
      ))}
    </ul>
  );
}
