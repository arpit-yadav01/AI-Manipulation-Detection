# # backend/app/video/aggregator.py

# ML_FAKE_THRESHOLD = 0.6
# ELA_SUSPICIOUS_THRESHOLD = 15


# def aggregate_frames(frame_results: list[dict]) -> dict:
#     """
#     Aggregate frame-level predictions into video-level stats.
#     """

#     if not frame_results:
#         return {
#             "avg_fake_probability": 0.0,
#             "frames_analyzed": 0,
#             "high_risk_frames": 0,
#             "ela_suspicious_frames": 0
#         }

#     total_frames = len(frame_results)

#     # --- ML aggregation ---
#     fake_probs = [f["ml_fake_probability"] for f in frame_results]
#     avg_fake = sum(fake_probs) / total_frames

#     high_risk_frames = sum(
#         1 for f in frame_results
#         if f["ml_fake_probability"] >= ML_FAKE_THRESHOLD
#     )

#     # --- ELA aggregation ---
#     ela_suspicious_frames = sum(
#         1 for f in frame_results
#         if f.get("ela_score", 0) >= ELA_SUSPICIOUS_THRESHOLD
#     )

#     return {
#         "avg_fake_probability": round(avg_fake, 3),
#         "frames_analyzed": total_frames,
#         "high_risk_frames": high_risk_frames,
#         "ela_suspicious_frames": ela_suspicious_frames
#     }


ML_FAKE_THRESHOLD = 0.6
ELA_SUSPICIOUS_THRESHOLD = 15


def aggregate_frames(frame_results: list[dict]) -> dict:
    """
    Aggregate frame-level predictions into video-level stats.
    VIDEO_V2.1 — band-aware aggregation.
    """

    if not frame_results:
        return {
            "avg_fake_probability": 0.0,
            "frames_analyzed": 0,
            "high_risk_frames": 0,
            "ela_suspicious_frames": 0,
            "strong_fake_frames": 0,
        }

    total_frames = len(frame_results)

    # --- ML aggregation ---
    fake_probs = [f["ml_fake_probability"] for f in frame_results]
    avg_fake = sum(fake_probs) / total_frames

    high_risk_frames = sum(
        1 for f in frame_results
        if f["confidence_band"] in ("LIKELY_FAKE", "STRONG_FAKE")
    )

    strong_fake_frames = sum(
        1 for f in frame_results
        if f["confidence_band"] == "STRONG_FAKE"
    )

    # --- ELA aggregation ---
    ela_suspicious_frames = sum(
        1 for f in frame_results
        if f.get("ela_score", 0) >= ELA_SUSPICIOUS_THRESHOLD
    )

    return {
        "avg_fake_probability": round(avg_fake, 3),
        "frames_analyzed": total_frames,
        "high_risk_frames": high_risk_frames,
        "strong_fake_frames": strong_fake_frames,
        "ela_suspicious_frames": ela_suspicious_frames,
    }
