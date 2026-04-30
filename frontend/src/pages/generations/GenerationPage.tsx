import CreateGenerationForm from "./components/CreateGenerationForm";
import GenerationList from "./components/GenerationList";

export default function GenerationPage() {
  return (
    <div>
      <h1 className="text-2xl">generations</h1>
      <GenerationList />
      <hr />
      <CreateGenerationForm />
    </div>
  );
}
