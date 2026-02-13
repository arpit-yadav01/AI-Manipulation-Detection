# def fuse_image_signals(
#     ela_score: float,
#     ml_fake_prob: float,
#     prnu: dict | None,
#     ai: dict | None,
#     exif: dict | None
# ):
#     """
#     ML-PRIMARY IMAGE FUSION ENGINE
#     - ML decides verdict
#     - PRNU / EXIF adjust confidence
#     - NEVER touches video jobs
#     """

#     # -------------------------------
#     # 1️⃣ AI GENERATED OVERRIDE
#     # -------------------------------
#     if ai and ai.get("ai_generated_prob", 0) > 0.8:
#         return {
#             "verdict": "LIKELY_FAKE",
#             "confidence": round(ai["ai_generated_prob"], 2),
#             "signals": {
#                 "reason": "AI-generated image detected",
#                 "ai_generated_prob": round(ai["ai_generated_prob"], 2)
#             }
#         }

#     # -------------------------------
#     # 2️⃣ ML DECIDES VERDICT
#     # -------------------------------
#     if ml_fake_prob >= 0.5:
#         verdict = "LIKELY_FAKE"
#         base_confidence = ml_fake_prob
#     else:
#         verdict = "LIKELY_REAL"
#         base_confidence = 1 - ml_fake_prob

#     # -------------------------------
#     # 3️⃣ CONFIDENCE BOOSTERS
#     # -------------------------------
#     confidence = base_confidence

#     if prnu and prnu.get("prnu_strength", 0) > 50:
#         confidence += 0.10

#     if exif:
#         confidence += 0.05

#     confidence = min(confidence, 0.95)

#     return {
#         "verdict": verdict,
#         "confidence": round(confidence, 2),
#         "signals": {
#             "ml_fake_probability": round(ml_fake_prob, 2),
#             "prnu_strength": prnu.get("prnu_strength") if prnu else None,
#             "exif_present": bool(exif)
#         }
#     }

def fuse_image_signals(
    ela_score: float,
    ml_fake_prob: float,
    prnu,
    ai,
    exif
):
    """
    Final image authenticity fusion engine.
    Conservative, explainable, interview-grade.
    """

    signals = {}

    # -------------------------
    # ML signal
    # -------------------------
    ml_fake_prob = float(ml_fake_prob)
    signals["ml_fake_probability"] = round(ml_fake_prob, 3)

    # -------------------------
    # PRNU signal (FIXED SEMANTICS)
    # -------------------------
    if isinstance(prnu, (int, float)):
        prnu_strength = float(prnu)
    elif isinstance(prnu, dict):
        prnu_strength = prnu.get("strength")
    else:
        prnu_strength = None

    signals["prnu_strength"] = (
        round(prnu_strength, 3) if prnu_strength is not None else None
    )

    # -------------------------
    # EXIF signal
    # -------------------------
    signals["exif_present"] = bool(exif and len(exif) > 0)

    # -------------------------
    # Fusion score
    # -------------------------
    score = 0.0

    # ML contribution (dominant but not absolute)
    if ml_fake_prob >= 0.6:
        score += 0.6
    elif ml_fake_prob >= 0.3:
        score += 0.3

    # ELA contribution (CRITICAL FIX)
    if ela_score >= 8.0:
        score += 0.2

    # PRNU contribution (FIXED DIRECTION)
    if prnu_strength is not None and prnu_strength >= 60.0:
        score += 0.2

    # EXIF missing → weak signal
    if not signals["exif_present"]:
        score += 0.1

    # -------------------------
    # Final Verdict
    # -------------------------
    if score >= 0.7:
        verdict = "LIKELY_FAKE"
        confidence = min(0.6 + score, 0.95)

    elif score >= 0.4:
        verdict = "SUSPICIOUS"
        confidence = 0.7

    else:
        verdict = "LIKELY_REAL"
        confidence = max(0.9, 1.0 - ml_fake_prob)

    return {
        "verdict": verdict,
        "confidence": round(confidence, 2),
        "signals": signals
    }
