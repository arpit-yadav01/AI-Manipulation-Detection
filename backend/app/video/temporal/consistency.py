def compute_temporal_stability(frame_results):
    if len(frame_results) < 2:
        return {
            "stability_score": 1.0,
            "verdict": "insufficient_frames"
        }

    diffs = []
    for i in range(len(frame_results) - 1):
        diff = abs(
            frame_results[i]["ml_fake_probability"]
            - frame_results[i + 1]["ml_fake_probability"]
        )
        diffs.append(diff)

    avg_diff = sum(diffs) / len(diffs)

    verdict = "stable" if avg_diff < 0.15 else "unstable"

    return {
        "stability_score": round(1 - avg_diff, 2),
        "verdict": verdict
    }
