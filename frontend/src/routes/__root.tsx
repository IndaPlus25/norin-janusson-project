import { Outlet, createRootRoute, Link } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/router-devtools";
import { connectMqtt, disconnectMqtt } from "../lib/mqtt";
import { useEffect } from "react";
import { MqttSync } from "../lib/mqttSync";

export const Route = createRootRoute({
  component: RootLayout,
});

function RootLayout() {
  useEffect(() => {
    connectMqtt();
    return () => disconnectMqtt();
  }, []);

  return (
    <>
      <MqttSync />
      <nav className="p-4 border-b flex gap-4">
        <Link to="/" className="[&.active]:font-bold">
          Home.
        </Link>
        <Link to="/observation-sensor" className="[&.active]:font-bold">
          Observation Sensors.
        </Link>
        <Link to="/generation" className="[&.active]:font-bold">
          Generation.
        </Link>
        <Link to="/car-observation" className="[&.active]:font-bold">
          Car Observation.
        </Link>
      </nav>
      <main className="p-4">
        <Outlet />
      </main>
      <TanStackRouterDevtools />
    </>
  );
}
