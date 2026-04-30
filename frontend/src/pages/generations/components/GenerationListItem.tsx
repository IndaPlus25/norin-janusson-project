import { useState } from "react";
import type { GenerationResponseDto } from "../../../types/generationTypes";
import CarList from "./CarList";
import { useAppStore } from "../../../stores/appStore";

type Props = {
  generation: GenerationResponseDto;
};

export default function GenerationListItem({ generation }: Props) {
  const [isOpened, setIsOpened] = useState(false);
  const { selectGeneration, unselectGeneration, selectedGenerationIds } =
    useAppStore();
  const isSelected = selectedGenerationIds.includes(generation.id);

  return (
    <li>
      <p>id: {generation.id}</p>
      <p>created_at: {generation.created_at}</p>
      <p>name: {generation.name}</p>

      <button onClick={() => setIsOpened((prev) => !prev)}>
        {isOpened ? "close" : "view"}
      </button>

      {isOpened && (
        <>
          {isSelected ? (
            <button onClick={() => unselectGeneration(generation.id)}>
              unselect
            </button>
          ) : (
            <button onClick={() => selectGeneration(generation.id)}>
              select
            </button>
          )}
          <CarList generationId={generation.id} />
        </>
      )}
    </li>
  );
}
