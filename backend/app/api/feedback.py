from fastapi import APIRouter
from pydantic import BaseModel
from app.core.db import mongo
from app.video.weight_learning import update_weights_from_feedback

router = APIRouter()


class FeedbackRequest(BaseModel):
    job_id: str
    true_label: str  # "AI_GENERATED" or "LIKELY_REAL"


@router.post("/submit")
def submit_feedback(request: FeedbackRequest):

    record = mongo.results.find_one({"job_id": request.job_id})

    if not record or not record.get("result"):
        return {"status": "error", "message": "Job not found"}

    update_weights_from_feedback(
        job_result=record["result"],
        ground_truth=request.true_label,
    )

    mongo.results.update_one(
        {"job_id": request.job_id},
        {"$set": {"ground_truth": request.true_label}}
    )

    return {"status": "weights_updated"}