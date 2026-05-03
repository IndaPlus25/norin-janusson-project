import { useState } from "react";
import type { CarResponseDto } from "../../../types/carTypes";
import { useAppStore } from "../../../stores/appStore";

type Props = {
  car: CarResponseDto;
};

export default function CarListItem({ car }: Props) {
  const [isOpened, setIsOpened] = useState(false);
  const { selectCar, unselectCar, selectedCarIdsByGeneration } = useAppStore();
  const isSelected =
    selectedCarIdsByGeneration[car.generation_id]?.includes(car.id) ?? false;

  return (
    <li>
      <p>id: {car.id}</p>
      <p>name: {car.name}</p>
      <button onClick={() => setIsOpened((prev) => !prev)}>
        {isOpened ? "close" : "view"}
      </button>

      {isOpened && (
        <>
          {isSelected ? (
            <button onClick={() => unselectCar(car.generation_id, car.id)}>
              unselect
            </button>
          ) : (
            <button onClick={() => selectCar(car.generation_id, car.id)}>
              select
            </button>
          )}

          <h4>TPMS sensors</h4>
          {car.tpms_sensor_ids.length === 0 ? (
            <p>No TPMS sensors</p>
          ) : (
            <ul>
              {car.tpms_sensor_ids.map((tpms_sensor_id) => (
                <li key={tpms_sensor_id}>
                  <p>tpms sensor id: {tpms_sensor_id}</p>
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </li>
  );
}
