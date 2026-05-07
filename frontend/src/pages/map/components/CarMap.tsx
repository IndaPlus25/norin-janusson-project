import { MapContainer, TileLayer, Marker, Polyline } from "react-leaflet";
import L from "leaflet";
import icon from "leaflet/dist/images/marker-icon.png";
import { Fragment, useMemo } from "react";
import { useAppStore } from "../../../stores/appStore";
import { useRecentCarObservationsForGenerations } from "../../../services/carObservations/carObservation.hooks";

L.Marker.prototype.options.icon = L.icon({
  iconUrl: icon,
});

const CAR_COLORS = ["red", "blue", "green", "orange", "brown"];

function colorForCar(carId: number): string {
  return CAR_COLORS[carId % CAR_COLORS.length];
}

export default function CarMap() {
  const selectedGenerationIds = useAppStore((s) => s.selectedGenerationIds);
  const selectedCarIdsByGen = useAppStore((s) => s.selectedCarIdsByGeneration);
  const selectedMaxAgeMs = useAppStore((s) => s.selectedMaxAgeMs);

  const queries = useRecentCarObservationsForGenerations(
    selectedGenerationIds,
    selectedMaxAgeMs,
  );

  const selectedCarIds = useMemo(() => {
    const set = new Set<number>();
    for (const gen of selectedGenerationIds) {
      for (const id of selectedCarIdsByGen[gen] ?? []) set.add(id);
    }
    return set;
  }, [selectedGenerationIds, selectedCarIdsByGen]);

  const observations = useMemo(
    () =>
      queries
        .flatMap((q) => q.data ?? [])
        .filter((o) => selectedCarIds.has(o.car_id)),
    [queries, selectedCarIds],
  );

  return (
    <MapContainer
      center={[0, 0]}
      zoom={0}
      style={{ height: "500px", width: "100%" }}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {observations.map((obs) => {
        const path = obs.path_coordinates;
        if (!path || path.length === 0) return null;
        const color = colorForCar(obs.car_id);
        const end = path[path.length - 1];
        return (
          <Fragment key={obs.id}>
            <Polyline positions={path} pathOptions={{ color }} />
            <Marker position={end} />
          </Fragment>
        );
      })}
    </MapContainer>
  );
}
