


# from app.core.db import mongo
# from app.utils.ela import compute_ela_score
# from app.utils.exif import extract_exif
# from app.utils.prnu import compute_prnu_score
# from app.models.image_classifier import ImageAuthenticityModel
# from app.services.authenticity_engine import fuse_image_signals
# from app.explainability.gradcam_utils import generate_gradcam
# from app.models.image.registry import get_active_image_model_version

# MODEL_PATH = "/app/app/models/image_auth_model.pt"

# _model = None


# def get_model():
#     global _model
#     if _model is None:
#         _model = ImageAuthenticityModel(MODEL_PATH)
#     return _model


# def process_image(job_id: str, image_path: str):
#     try:
#         # -----------------------------
#         # 1️⃣ Core detectors (MUST WORK)
#         # -----------------------------
#         ela_score = compute_ela_score(image_path)
#         exif = extract_exif(image_path)
#         prnu_score = compute_prnu_score(image_path)

#         model_wrapper = get_model()
#         ml_fake_prob = model_wrapper.predict(image_path)

#         # -----------------------------
#         # 2️⃣ Fusion (RAW OUTPUT)
#         # -----------------------------
#         fused_raw = fuse_image_signals(
#             ela_score=ela_score,
#             ml_fake_prob=ml_fake_prob,
#             prnu=prnu_score,
#             ai=None,
#             exif=exif
#         )

#         # -----------------------------
#         # 🔒 NORMALIZE FUSION OUTPUT
#         # -----------------------------
#         if isinstance(fused_raw, dict):
#             fused = fused_raw
#         else:
#             # Backward compatibility (older fusion versions)
#             fused = {
#                 "verdict": "LOW_CONFIDENCE",
#                 "confidence": float(fused_raw),
#                 "signals": {
#                     "ml_fake_probability": round(float(ml_fake_prob), 3),
#                     "prnu_strength": prnu_score,
#                     "exif_present": bool(exif)
#                 }
#             }

#         # -----------------------------
#         # 3️⃣ Grad-CAM (NON-BLOCKING)
#         # -----------------------------
#         try:
#             gradcam_path = generate_gradcam(
#                 image_path=image_path,
#                 model=model_wrapper.get_raw_model(),
#                 device=model_wrapper.device
#             )
#         except Exception as cam_err:
#             print("⚠️ GradCAM failed:", cam_err)
#             gradcam_path = None

#         # -----------------------------
#         # 4️⃣ SAVE RESULT (SINGLE SOURCE OF TRUTH)
#         # -----------------------------
#         mongo.results.update_one(
#             {"job_id": job_id},
#             {
#                 "$set": {
#                     "status": "done",
#                     "result": {
#                         "type": "image",
#                         "ela_score": round(float(ela_score), 3),
#                         "ml_fake_probability": round(float(ml_fake_prob), 3),
#                         "final_verdict": {
#                             "verdict": fused["verdict"],
#                             "confidence": fused["confidence"]
#                         },
#                         "model_version": get_active_image_model_version(),

#                         "signals": fused["signals"],
#                         "prnu_score": prnu_score,
#                         "exif": exif,
#                         "ela_heatmap": gradcam_path
#                     }
#                 }
#             },
#             upsert=True
#         )

#     except Exception as e:
#         mongo.results.update_one(
#             {"job_id": job_id},
#             {
#                 "$set": {
#                     "status": "error",
#                     "error": str(e)
#                 }
#             },
#             upsert=True
#         )





from app.core.db import mongo
from app.utils.ela import compute_ela_score
from app.utils.exif import extract_exif
from app.utils.prnu import compute_prnu_score
from app.models.image_classifier import ImageAuthenticityModel
from app.services.authenticity_engine import fuse_image_signals
from app.explainability.gradcam_utils import generate_gradcam
from app.models.image.registry import get_active_image_model_version
from app.models.image.registry import get_active_image_model_dir


_model = None


def get_model():
    global _model
    if _model is None:
        model_dir = get_active_image_model_dir()
        model_path = model_dir / "image_auth_model.pt"
        _model = ImageAuthenticityModel(str(model_path))
    return _model



def process_image(job_id: str, image_path: str):
    try:
        # -----------------------------
        # 1️⃣ Core detectors (MUST WORK)
        # -----------------------------
        ela_score = compute_ela_score(image_path)
        exif = extract_exif(image_path)
        prnu_score = compute_prnu_score(image_path)

        model_wrapper = get_model()
        ml_fake_prob = model_wrapper.predict(image_path)

        # -----------------------------
        # 2️⃣ Fusion (RAW OUTPUT)
        # -----------------------------
        fused_raw = fuse_image_signals(
            ela_score=ela_score,
            ml_fake_prob=ml_fake_prob,
            prnu=prnu_score,
            ai=None,
            exif=exif
        )

        # -----------------------------
        # 🔒 NORMALIZE FUSION OUTPUT
        # -----------------------------
        if isinstance(fused_raw, dict):
            fused = fused_raw
        else:
            # Backward compatibility (older fusion versions)
            fused = {
                "verdict": "LOW_CONFIDENCE",
                "confidence": float(fused_raw),
                "signals": {
                    "ml_fake_probability": round(float(ml_fake_prob), 3),
                    "prnu_strength": prnu_score,
                    "exif_present": bool(exif)
                }
            }

        # -----------------------------
        # 3️⃣ Grad-CAM (NON-BLOCKING)
        # -----------------------------
        try:
            gradcam_path = generate_gradcam(
                image_path=image_path,
                model=model_wrapper.get_raw_model(),
                device=model_wrapper.device
            )
        except Exception as cam_err:
            print("⚠️ GradCAM failed:", cam_err)
            gradcam_path = None

        # -----------------------------
        # 4️⃣ SAVE RESULT (SINGLE SOURCE OF TRUTH)
        # -----------------------------
        mongo.results.update_one(
            {"job_id": job_id},
            {
                "$set": {
                    "status": "done",
                    "result": {
                        "type": "image",
                        "ela_score": round(float(ela_score), 3),
                        "ml_fake_probability": round(float(ml_fake_prob), 3),
                        "final_verdict": {
                            "verdict": fused["verdict"],
                            "confidence": fused["confidence"]
                        },
                        "model_version": get_active_image_model_version(),

                        "signals": fused["signals"],
                        "prnu_score": prnu_score,
                        "exif": exif,
                        "ela_heatmap": gradcam_path
                    }
                }
            },
            upsert=True
        )

    except Exception as e:
        mongo.results.update_one(
            {"job_id": job_id},
            {
                "$set": {
                    "status": "error",
                    "error": str(e)
                }
            },
            upsert=True
        )
