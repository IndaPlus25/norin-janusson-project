import { createFileRoute } from "@tanstack/react-router";
import ObservationSensorPage from "../pages/observationSensors/ObservationSensorPage";

export const Route = createFileRoute("/observation-sensor")({
  component: () => <ObservationSensorPage />,
});
