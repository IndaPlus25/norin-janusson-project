import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: () => (
    <h1 className="text-2xl">
      Welcome to p20 h4ck3r c3n7r4l, no n00bs alowed past this point
    </h1>
  ),
});
