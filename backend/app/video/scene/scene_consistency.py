import numpy as np
import torch
import clip
from PIL import Image
from sklearn.metrics.pairwise import cosine_distances
from typing import List, Dict

# -------------------------------------------------
# Model setup (CPU-safe)
# -------------------------------------------------

DEVICE = "cpu"
MODEL_NAME = "ViT-B/32"

_clip_model, _clip_preprocess = clip.load(MODEL_NAME, device=DEVICE)
_clip_model.eval()


# -------------------------------------------------
# Helper: extract global scene embedding
# -------------------------------------------------

def extract_scene_embedding(image_path: str):
    try:
        img = Image.open(image_path).convert("RGB")
        img_tensor = _clip_preprocess(img).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            emb = _clip_model.encode_image(img_tensor)

        emb = emb / emb.norm(dim=-1, keepdim=True)
        return emb.squeeze(0).cpu().numpy()

    except Exception:
        return None


# -------------------------------------------------
# STEP 3.2.1 — Scene consistency analyzer
# -------------------------------------------------

def analyze_scene_consistency(
    frame_results: List[Dict],
    min_frames: int = 6,
) -> Dict:
    """
    Detects background / scene drift across video frames.

    Returns:
    - avg_drift
    - max_drift
    - verdict
    """

    embeddings = []

    for frame in frame_results:
        path = frame.get("frame_path_local") or frame.get("path")

        if not path:
            continue

        emb = extract_scene_embedding(path)
        if emb is not None:
            embeddings.append(emb)

    if len(embeddings) < min_frames:
        return {
            "available": False,
            "reason": "insufficient_frames",
        }

    E = np.stack(embeddings)

    # -----------------------------------------
    # Drift computation (temporal)
    # -----------------------------------------
    drifts = []

    for i in range(1, len(E)):
        d = cosine_distances(
            E[i - 1].reshape(1, -1),
            E[i].reshape(1, -1),
        )[0][0]
        drifts.append(float(d))

    avg_drift = float(np.mean(drifts))
    max_drift = float(np.max(drifts))

    # -----------------------------------------
    # Verdict (conservative thresholds)
    # -----------------------------------------
    if avg_drift > 0.30 or max_drift > 0.55:
        verdict = "unstable"
    elif avg_drift > 0.18:
        verdict = "mild_drift"
    else:
        verdict = "stable"

    return {
        "available": True,
        "avg_drift": round(avg_drift, 3),
        "max_drift": round(max_drift, 3),
        "frames_used": len(embeddings),
        "verdict": verdict,
    }
