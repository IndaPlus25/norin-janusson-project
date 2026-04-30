import { useState } from "react";
import { useFetchObservationSensors } from "../../../lib/observationSensors/observationSensor.hooks";
import ObservationSensorListItem from "./ObservationSensorListItem";

export default function ObservationSensorList() {
  const [shown, setShown] = useState(false);
  const { data, isLoading, error } = useFetchObservationSensors();

  return (
    <section>
      <button onClick={() => setShown((s) => !s)}>
        {shown ? "hide" : "show"} observation sensors
      </button>
      {shown && isLoading && <p>loading...</p>}
      {shown && error && <p>error: {error.message}</p>}
      {shown && data && data.length === 0 && <p>no sensors</p>}
      {shown && data && data.length > 0 && (
        <ul>
          {data.map((sensor) => (
            <ObservationSensorListItem key={sensor.id} sensor={sensor} />
          ))}
        </ul>
      )}
    </section>
  );
}
