from app.core.db import mongo
from pymongo import ReturnDocument

# ============================================================
# DEFAULT CONFIG
# ============================================================

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


# ============================================================
# GET REGISTRY
# ============================================================

def get_weight_registry():
    """
    Fetch adaptive weights from Mongo.
    If not present, initialize default registry.
    """

    registry = mongo.results.find_one({"type": "weight_registry"})

    if not registry:
        registry = {
            "type": "weight_registry",
            "version": "v1",
            "weights": DEFAULT_WEIGHTS.copy(),
        }
        mongo.results.insert_one(registry)

    return registry["weights"]


# ============================================================
# UPDATE FROM SUPERVISED FEEDBACK
# ============================================================

def update_weights_from_feedback(job_result: dict, ground_truth: str):
    """
    Update weights using supervised ground truth.
    Only updates signals that have anomaly scores.
    """

    registry = mongo.results.find_one({"type": "weight_registry"})

    if not registry:
        return DEFAULT_WEIGHTS

    weights = registry["weights"]

    predicted = job_result["final_verdict"]["verdict"]
    signal_breakdown = job_result["final_verdict"]["signal_breakdown"]

    # Was prediction correct?
    correct = predicted == ground_truth

    for signal_name, details in signal_breakdown.items():

        if signal_name not in weights:
            continue

        if not isinstance(details, dict):
            continue

        anomaly = details.get("anomaly", 0.0)

        # If prediction correct → reward signal
        # If incorrect → penalize signal
        alignment = anomaly if correct else -anomaly

        updated_weight = weights[signal_name] + LEARNING_RATE * alignment

        # Clamp for safety
        updated_weight = max(MIN_WEIGHT, min(MAX_WEIGHT, updated_weight))

        weights[signal_name] = round(updated_weight, 4)

    mongo.results.find_one_and_update(
        {"type": "weight_registry"},
        {"$set": {"weights": weights}},
        return_document=ReturnDocument.AFTER,
    )

    return weights