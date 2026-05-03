import { useState, type SyntheticEvent } from "react";
import { useCreateObservationSensor } from "../../../services/observationSensors/observationSensor.hooks";
import type { CreateObservationSensorDto } from "../../../types/observationSensorTypes";
import { EPSG } from "../../../types/enums";

const initial: CreateObservationSensorDto = {
  id: "",
  name: "",
  lat: 0,
  lng: 0,
  address: "",
  epsg: EPSG.STANDARD,
};

const EPSG_OPTIONS: { label: string; value: EPSG }[] = [
  { label: "WGS84 (4326)", value: EPSG.STANDARD },
  { label: "Web Mercator (3857)", value: EPSG.WEB_MERCATOR },
  { label: "SWEREF99 TM (3006)", value: EPSG.SWEREF99_TM },
  { label: "ETRS89 (4258)", value: EPSG.ETRS89 },
];

export default function CreateObservationSensorForm() {
  const [form, setForm] = useState<CreateObservationSensorDto>(initial);
  const { mutate, isPending, error } = useCreateObservationSensor();

  function handleSubmit(e: SyntheticEvent<HTMLFormElement>) {
    e.preventDefault();
    const id = form.id.trim();
    if (!id) return;
    mutate(
      { ...form, id },
      {
        onSuccess: () => setForm(initial),
      },
    );
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>create observation sensor</h2>
      <p>
        <label>
          id{" "}
          <input
            required
            minLength={1}
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
      <p>
        <label>
          epsg{" "}
          <select
            value={form.epsg}
            onChange={(e) =>
              setForm({ ...form, epsg: Number(e.target.value) as EPSG })
            }
          >
            {EPSG_OPTIONS.map((o) => (
              <option key={o.value} value={o.value}>
                {o.label}
              </option>
            ))}
          </select>
        </label>
      </p>
      <button type="submit" disabled={isPending}>
        {isPending ? "creating..." : "create"}
      </button>
      {error && <p>error: {error.message}</p>}
    </form>
  );
}
