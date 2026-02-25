from app.core.db import get_database
from pymongo import ReturnDocument

DEFAULT_WEIGHTS = {
    "temporal": 0.10,
    "motion": 0.08,
    "identity": 0.09,
    "geometry": 0.07,
    "av_sync": 0.08,
    "gan": 0.04,
    "video_ml": 0.15,
}

LEARNING_RATE = 0.02
MIN_WEIGHT = 0.02
MAX_WEIGHT = 0.25


def get_weight_registry():
    db = get_database()
    registry = db.results.find_one({"type": "weight_registry"})

    if not registry:
        registry = {
            "type": "weight_registry",
            "version": "v1",
            "weights": DEFAULT_WEIGHTS,
        }
        db.results.insert_one(registry)

    return registry["weights"]


def update_weights_from_feedback(job_result: dict, ground_truth: str):
    """
    Update weights based on supervised ground truth.
    """

    db = get_database()
    registry = db.results.find_one({"type": "weight_registry"})

    if not registry:
        return

    weights = registry["weights"]

    predicted = job_result["final_verdict"]["verdict"]
    signal_breakdown = job_result["final_verdict"]["signal_breakdown"]

    # Determine if prediction was correct
    correct = predicted == ground_truth

    for signal_name, details in signal_breakdown.items():
        if signal_name in weights and isinstance(details, dict):
            anomaly = details.get("anomaly", 0)
            impact = details.get("effective_impact", 0)

            # signal alignment score
            alignment = anomaly if correct else -anomaly

            updated_weight = weights[signal_name] + LEARNING_RATE * alignment

            # clamp
            updated_weight = max(MIN_WEIGHT, min(MAX_WEIGHT, updated_weight))
            weights[signal_name] = round(updated_weight, 4)

    db.results.find_one_and_update(
        {"type": "weight_registry"},
        {"$set": {"weights": weights}},
        return_document=ReturnDocument.AFTER,
    )

    return weights