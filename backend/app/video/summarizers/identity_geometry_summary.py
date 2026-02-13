def summarize_identity(signal: dict) -> float:
    """
    Converts identity similarity + variance into anomaly score [0,1]
    """

    if not signal or signal.get("mean_similarity") is None:
        return 0.0

    mean_sim = float(signal["mean_similarity"])
    variance = float(signal["variance"])

    # Penalize low similarity
    similarity_penalty = max(0.0, (0.9 - mean_sim) / 0.3)

    # Penalize high variance
    variance_penalty = min(variance / 0.05, 1.0)

    anomaly = (similarity_penalty + variance_penalty) / 2.0

    return max(0.0, min(anomaly, 1.0))


def summarize_geometry(signal: dict) -> float:
    """
    Converts head pose temporal drift into anomaly score [0,1]
    """

    if not signal or not signal.get("available"):
        return 0.0

    delta_var = signal.get("delta_variance", {})
    max_jump = signal.get("max_jump", {})

    # Average rotational jitter
    jitter_score = (
        delta_var.get("yaw", 0)
        + delta_var.get("pitch", 0)
        + delta_var.get("roll", 0)
    ) / 3.0

    jitter_penalty = min(jitter_score / 4.0, 1.0)

    # Max sudden jump
    jump_score = (
        max_jump.get("yaw", 0)
        + max_jump.get("pitch", 0)
        + max_jump.get("roll", 0)
    ) / 3.0

    jump_penalty = min(jump_score / 25.0, 1.0)

    anomaly = (jitter_penalty + jump_penalty) / 2.0

    return max(0.0, min(anomaly, 1.0))
