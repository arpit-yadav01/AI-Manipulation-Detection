import face_recognition
import numpy as np
from typing import List


def compute_identity_consistency(frame_paths: List[str]):
    """
    Detects identity drift across frames using face embeddings
    """

    embeddings = []

    for frame_path in frame_paths:
        try:
            image = face_recognition.load_image_file(frame_path)
            encodings = face_recognition.face_encodings(image)

            if not encodings:
                continue  # no face detected

            embeddings.append(encodings[0])

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
