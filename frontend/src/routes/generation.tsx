import { createFileRoute } from "@tanstack/react-router";
import GenerationPage from "../pages/generation/GenerationPage";

export const Route = createFileRoute("/generation")({
  component: () => <GenerationPage />,
});
