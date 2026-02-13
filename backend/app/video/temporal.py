def compute_temporal_stability(frame_results):
    probs = [f["ml_fake_probability"] for f in frame_results]

    if len(probs) < 3:
        return {"stability_score": 1.0}

    diffs = [abs(probs[i] - probs[i-1]) for i in range(1, len(probs))]
    instability = sum(diffs) / len(diffs)

    stability = max(0.0, 1 - instability)

    return {"stability_score": round(stability, 2)}
