import { useFetchCarsForGeneration } from "../../../services/cars/car.hooks";
import CarListItem from "./CarListItem";

type Props = {
  generationId: number;
};

export default function CarList({ generationId }: Props) {
  const query = useFetchCarsForGeneration(generationId);

  const isLoading = query.isLoading;
  const error = query.error;

  if (isLoading) return <p>loading...</p>;
  if (error) return <p>error: {error.message}</p>;

  const cars = query.data ?? [];

  if (cars.length === 0) return <p>no cars in generation</p>;

  return (
    <ul>
      {cars.map((car) => (
        <CarListItem key={car.id} car={car} />
      ))}
    </ul>
  );
}
