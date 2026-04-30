import { createFileRoute } from "@tanstack/react-router";
import CarObservationPage from "../pages/carObservations/CarObservationPage";

export const Route = createFileRoute("/car-observation")({
  component: () => <CarObservationPage />,
});
