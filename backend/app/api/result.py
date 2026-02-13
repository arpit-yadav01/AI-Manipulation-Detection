# from fastapi import APIRouter
# from app.core.db import mongo

# router = APIRouter()


# @router.get("/{job_id}")
# async def get_result(job_id: str):
#     doc = mongo.results.find_one(
#         {"job_id": job_id},
#         {"_id": 0}
#     )

#     if not doc:
#         return {"status": "processing", "result": None}

#     status = doc.get("status")

#     # ✅ RETURN REAL ERROR
#     if status == "error":
#         return {
#             "status": "error",
#             "error": doc.get("error", "Unknown worker error"),
#             "result": None
#         }

#     if status != "done":
#         return {"status": status, "result": None}

#     return {
#         "status": "done",
#         "result": doc.get("result")
#     }


# backend/app/api/result.py

from fastapi import APIRouter
from app.core.db import mongo
import os

router = APIRouter()


@router.get("/{job_id}")
async def get_result(job_id: str):
    """
    Fetch analysis result for image or video job.

    RESPONSIBILITIES:
    - Return job status
    - Surface worker errors
    - Attach video_url for frontend playback (if video)
    """

    doc = mongo.results.find_one(
        {"job_id": job_id},
        {"_id": 0}
    )

    # ----------------------------
    # Job not found / still queued
    # ----------------------------
    if not doc:
        return {
            "status": "processing",
            "result": None
        }

    status = doc.get("status")

    # ----------------------------
    # Worker error (surface clearly)
    # ----------------------------
    if status == "error":
        return {
            "status": "error",
            "error": doc.get("error", "Unknown worker error"),
            "result": None
        }

    # ----------------------------
    # Still running
    # ----------------------------
    if status != "done":
        return {
            "status": status,
            "result": None
        }

    # ----------------------------
    # DONE — build final payload
    # ----------------------------
    result = doc.get("result", {})

    # 🔥 VIDEO PLAYBACK FIX
    video_path = doc.get("video_path")
    if video_path:
        filename = os.path.basename(video_path)

        # Matches StaticFiles mount:
        # app.mount("/files", StaticFiles(directory="/app/datasets/uploads"))
        result["video_url"] = f"http://localhost:8000/files/videos/{filename}"

    return {
        "status": "done",
        "result": result
    }
