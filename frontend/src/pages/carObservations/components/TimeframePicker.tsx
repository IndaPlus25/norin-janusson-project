import { useAppStore } from "../../../stores/appStore";

const MS_PER_HOUR = 3_600_000;

export default function TimeframePicker() {
  const selectedMaxAgeMs = useAppStore((s) => s.selectedMaxAgeMs);
  const setSelectedMaxAgeMs = useAppStore((s) => s.setSelectedMaxAgeMs);

  const hours = selectedMaxAgeMs / MS_PER_HOUR;

  return (
    <p>
      <label>
        timeframe (hours):{" "}
        <input
          type="number"
          min={0}
          step="any"
          value={hours}
          onChange={(e) => {
            const next = Number(e.target.value);
            if (!Number.isFinite(next) || next <= 0) return;
            setSelectedMaxAgeMs(next * MS_PER_HOUR);
          }}
        />
      </label>
    </p>
  );
}
