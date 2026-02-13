
# from app.models.image_classifier import ImageAuthenticityModel
# from app.utils.ela import compute_ela_score
# from app.utils.exif import extract_exif

# # Load model once (IMPORTANT)
# _model = None


# def get_model():
#     global _model
#     if _model is None:
#         _model = ImageAuthenticityModel("/app/app/models/image_auth_model.pt")
#     return _model


# def get_confidence_band(prob: float) -> str:
#     """
#     Convert raw ML probability into semantic confidence bands.
#     VIDEO_V2.1 — reduces flickering & noise.
#     """
#     if prob < 0.30:
#         return "STRONG_REAL"
#     elif prob < 0.60:
#         return "UNCERTAIN"
#     elif prob < 0.85:
#         return "LIKELY_FAKE"
#     else:
#         return "STRONG_FAKE"


# def analyze_frame(frame_path: str) -> dict:
#     """
#     Analyze a single video frame using image pipeline logic.
#     """

#     # 1️⃣ ELA
#     ela_score = compute_ela_score(frame_path)

#     # 2️⃣ ML prediction
#     model = get_model()
#     ml_fake_prob = float(model.predict(frame_path))

#     # 3️⃣ Confidence band (NEW)
#     confidence_band = get_confidence_band(ml_fake_prob)

#     # 4️⃣ EXIF (mostly empty for frames, expected)
#     exif = extract_exif(frame_path)

#     return {
#         "ela_score": ela_score,
#         "ml_fake_probability": ml_fake_prob,
#         "confidence_band": confidence_band,
#         "exif": exif,
#     }







from app.models.image_classifier import ImageAuthenticityModel
from app.utils.ela import compute_ela_score
from app.utils.exif import extract_exif

from app.video.identity.face_embedder import extract_face_embedding
from app.video.geometry.head_pose import estimate_head_pose
from app.video.geometry.lighting import estimate_lighting


# -------------------------
# Load model once (IMPORTANT)
# -------------------------
_model = None


def get_model():
    global _model
    if _model is None:
        _model = ImageAuthenticityModel("/app/app/models/image_auth_model.pt")
    return _model


def get_confidence_band(prob: float) -> str:
    """
    Convert raw ML probability into semantic confidence bands.
    VIDEO_V2.1 — reduces flickering & noise.
    """
    if prob < 0.30:
        return "STRONG_REAL"
    elif prob < 0.60:
        return "UNCERTAIN"
    elif prob < 0.85:
        return "LIKELY_FAKE"
    else:
        return "STRONG_FAKE"


def analyze_frame(frame_path: str) -> dict:
    """
    Analyze a single video frame.
    SAFE: no verdicts, only signals.
    """

    # 1️⃣ ELA (compression artifacts)
    ela_score = compute_ela_score(frame_path)

    # 2️⃣ ML classifier
    model = get_model()
    ml_fake_prob = float(model.predict(frame_path))
    confidence_band = get_confidence_band(ml_fake_prob)

    # 3️⃣ EXIF (usually empty for video frames)
    exif = extract_exif(frame_path)

    # 4️⃣ Identity embedding (IN-MEMORY ONLY)
    face_embedding = extract_face_embedding(frame_path)

    # 5️⃣ Geometry — head pose
    head_pose = estimate_head_pose(frame_path)

    # 6️⃣ Lighting — asymmetry signal
    lighting = estimate_lighting(frame_path)

    # -------------------------
    # IMPORTANT:
    # DO NOT persist embeddings
    # -------------------------

    return {
        # Core signals
        "ela_score": float(ela_score),
        "ml_fake_probability": ml_fake_prob,
        "confidence_band": confidence_band,
        "exif": exif,

        # Geometry & lighting (Phase 2)
        "geometry": head_pose,
        "lighting": lighting,

        # ❌ face_embedding REMOVED from result
    }
