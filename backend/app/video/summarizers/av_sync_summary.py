# app/video/summarizers/av_sync_summary.py

def summarize_av_sync(
    av_sync_signal: dict | None,
    speech_signal: dict | None,
) -> float:
    """
    Converts AV sync into normalized anomaly score [0–1].

    Rules:
    - No audio → 0.0
    - No speech → 0.0
    - Insufficient data → 0.0
    - High correlation → low anomaly
    - Low correlation → high anomaly
    """

    if not isinstance(av_sync_signal, dict):
        return 0.0

    if not isinstance(speech_signal, dict):
        return 0.0

    # 🔒 Must have speech
    if not speech_signal.get("available"):
        return 0.0

    if not speech_signal.get("speech_present"):
        return 0.0

    verdict = av_sync_signal.get("verdict")
    corr = av_sync_signal.get("correlation")

    if verdict == "insufficient_data" or corr is None:
        return 0.0

    # Normalize correlation to anomaly
    # corr ∈ [-1,1]
    corr = max(-1.0, min(1.0, float(corr)))

    # Good sync → corr near 1
    # Anomaly = inverse of positive correlation
    anomaly = 1.0 - max(0.0, corr)

    # Reliability scaling using speech confidence
    speech_conf = float(speech_signal.get("confidence", 0.0))
    reliability = min(1.0, speech_conf)

    anomaly *= reliability

    return round(max(0.0, min(1.0, anomaly)), 3)
