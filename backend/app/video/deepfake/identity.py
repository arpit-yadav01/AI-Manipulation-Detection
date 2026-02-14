import torch
import numpy as np
from typing import List
from PIL import Image

from facenet_pytorch import MTCNN, InceptionResnetV1

# ------------------------------------------------------------
# Load FaceNet models once (CPU mode)
# ------------------------------------------------------------

device = torch.device("cpu")

mtcnn = MTCNN(keep_all=False, device=device)
resnet = InceptionResnetV1(pretrained="vggface2").eval().to(device)


# ============================================================
# IDENTITY CONSISTENCY
# ============================================================

def compute_identity_consistency(frame_paths: List[str]):
    """
    Detect identity drift using FaceNet embeddings
    """

    embeddings = []

    for frame_path in frame_paths:
        try:
            img = Image.open(frame_path).convert("RGB")

            face = mtcnn(img)

            if face is None:
                continue

            face = face.unsqueeze(0).to(device)
            emb = resnet(face).detach().cpu().numpy()[0]

            embeddings.append(emb)

        except Exception:
            continue

    if len(embeddings) < 2:
        return {
            "mean_similarity": None,
            "variance": None,
            "verdict": "insufficient_faces"
        }

    similarities = []
    base = embeddings[0]

    for emb in embeddings[1:]:
        sim = np.dot(base, emb) / (
            np.linalg.norm(base) * np.linalg.norm(emb)
        )
        similarities.append(sim)

    mean_sim = float(np.mean(similarities))
    variance = float(np.var(similarities))

    verdict = (
        "stable_identity"
        if mean_sim > 0.85 and variance < 0.02
        else "unstable_identity"
    )

    return {
        "mean_similarity": round(mean_sim, 3),
        "variance": round(variance, 3),
        "verdict": verdict
    }


# ============================================================
# IDENTITY → ANOMALY
# ============================================================

def summarize_identity(signal: dict) -> float:

    if not signal or signal.get("mean_similarity") is None:
        return 0.0

    mean_sim = float(signal["mean_similarity"])
    variance = float(signal["variance"])

    similarity_penalty = max(0.0, (0.9 - mean_sim) / 0.3)
    variance_penalty = min(variance / 0.05, 1.0)

    anomaly = (similarity_penalty + variance_penalty) / 2.0

    return max(0.0, min(anomaly, 1.0))


# ============================================================
# GEOMETRY → ANOMALY
# ============================================================

def summarize_geometry(signal: dict) -> float:

    if not signal or not signal.get("available"):
        return 0.0

    delta_var = signal.get("delta_variance", {})
    max_jump = signal.get("max_jump", {})

    jitter_score = (
        delta_var.get("yaw", 0)
        + delta_var.get("pitch", 0)
        + delta_var.get("roll", 0)
    ) / 3.0

    jitter_penalty = min(jitter_score / 4.0, 1.0)

    jump_score = (
        max_jump.get("yaw", 0)
        + max_jump.get("pitch", 0)
        + max_jump.get("roll", 0)
    ) / 3.0

    jump_penalty = min(jump_score / 25.0, 1.0)

    anomaly = (jitter_penalty + jump_penalty) / 2.0

    return max(0.0, min(anomaly, 1.0))
