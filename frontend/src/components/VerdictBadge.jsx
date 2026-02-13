export default function VerdictBadge({ verdict }) {
  let color = "#4CAF50"; // green
  let label = verdict;

  switch (verdict) {
    case "AI_GENERATED":
      color = "#E53935"; // red
      label = "AI GENERATED";
      break;

    case "INCONCLUSIVE":
      color = "#F9A825"; // amber
      label = "INCONCLUSIVE";
      break;

    case "LIKELY_REAL":
      color = "#43A047"; // green
      label = "LIKELY REAL";
      break;

    case "SUSPICIOUS":
      color = "#FB8C00"; // orange
      label = "SUSPICIOUS";
      break;

    default:
      color = "#757575"; // gray
      label = verdict || "UNKNOWN";
  }

  return (
    <span
      style={{
        padding: "6px 12px",
        borderRadius: 8,
        fontWeight: 600,
        fontSize: 13,
        letterSpacing: 0.4,
        color: "white",
        backgroundColor: color,
        display: "inline-block",
      }}
    >
      {label}
    </span>
  );
}
