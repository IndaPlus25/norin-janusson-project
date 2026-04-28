import CreateObservationSensorForm from "./components/CreateObservationSensorForm";
import ObservationSensorList from "./components/ObservationSensorList";

export default function ObservationSensorPage() {
  return (
    <div>
      <h1 className="text-2xl">observation sensors</h1>
      <ObservationSensorList />
      <hr />
      <CreateObservationSensorForm />
    </div>
  );
}
