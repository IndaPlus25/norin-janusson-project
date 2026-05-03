import { useFetchGenerations } from "../../../services/generations/generation.hooks";
import GenerationListItem from "./GenerationListItem";

export default function GenerationList() {
  const query = useFetchGenerations();

  const isLoading = query.isLoading;
  const error = query.error;

  if (isLoading) return <p>loading...</p>;
  if (error) return <p>error: {error.message}</p>;

  const generations = query.data ?? [];

  if (generations.length === 0) return <p>no generations</p>;

  return (
    <ul>
      {generations.map((generation) => (
        <GenerationListItem key={generation.id} generation={generation} />
      ))}
    </ul>
  );
}
