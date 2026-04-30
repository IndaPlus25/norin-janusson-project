import { useState, type SyntheticEvent } from "react";
import { useCreateObservationSensor } from "../../../lib/observationSensors/observationSensor.hooks";
import type { CreateObservationSensorDto } from "../../../types/observationSensorTypes";

const initial: CreateObservationSensorDto = {
  id: "",
  name: "",
  lat: 0,
  lng: 0,
  address: "",
};

export default function CreateObservationSensorForm() {
  const [form, setForm] = useState<CreateObservationSensorDto>(initial);
  const { mutate, isPending, error } = useCreateObservationSensor();

  function handleSubmit(e: SyntheticEvent<HTMLFormElement>) {
    e.preventDefault();
    mutate(form, {
      onSuccess: () => setForm(initial),
    });
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>create observation sensor</h2>
      <p>
        <label>
          id{" "}
          <input
            value={form.id}
            onChange={(e) => setForm({ ...form, id: e.target.value })}
          />
        </label>
      </p>
      <p>
        <label>
          name{" "}
          <input
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
        </label>
      </p>
      <p>
        <label>
          lat{" "}
          <input
            type="number"
            value={form.lat}
            onChange={(e) => setForm({ ...form, lat: Number(e.target.value) })}
          />
        </label>
      </p>
      <p>
        <label>
          lng{" "}
          <input
            type="number"
            value={form.lng}
            onChange={(e) => setForm({ ...form, lng: Number(e.target.value) })}
          />
        </label>
      </p>
      <p>
        <label>
          address{" "}
          <input
            value={form.address}
            onChange={(e) => setForm({ ...form, address: e.target.value })}
          />
        </label>
      </p>
      <button type="submit" disabled={isPending}>
        {isPending ? "creating..." : "create"}
      </button>
      {error && <p>error: {error.message}</p>}
    </form>
  );
}
