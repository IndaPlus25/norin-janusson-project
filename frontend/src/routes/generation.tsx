import { createFileRoute } from "@tanstack/react-router";
import GenerationPage from "../pages/generations/GenerationPage";

export const Route = createFileRoute("/generation")({
  component: () => <GenerationPage />,
});
