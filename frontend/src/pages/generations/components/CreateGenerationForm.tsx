import { useState, type SyntheticEvent } from "react";
import { useCreateGeneration } from "../../../services/generations/generation.hooks";
import type { CreateGenerationDto } from "../../../types/generationTypes";

const initial: CreateGenerationDto = {
  name: "",
};

export default function CreateGenerationForm() {
  const [form, setForm] = useState<CreateGenerationDto>(initial);
  const { mutate, isPending, error, isSuccess } = useCreateGeneration();

  function handleSubmit(e: SyntheticEvent<HTMLFormElement>) {
    e.preventDefault();
    mutate(form, {
      onSuccess: () => setForm(initial),
    });
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>create generation</h2>
      <p>
        <label>
          name{" "}
          <input
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
        </label>
      </p>
      <button type="submit" disabled={isPending}>
        {isPending ? "creating..." : "create"}
      </button>
      {error && <p>error: {error.message}</p>}
      {isSuccess && <p>created</p>}
    </form>
  );
}
