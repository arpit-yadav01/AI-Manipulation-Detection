from fastapi import APIRouter, UploadFile, File
from fastapi.concurrency import run_in_threadpool

from app.services.video_queue import enqueue_video_job

router = APIRouter()


@router.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):
    """
    Accepts a video upload and enqueues it for background analysis.
    MUST offload disk + Redis work to threadpool.
    """

    job_id = await run_in_threadpool(
        enqueue_video_job,
        file
    )

    return {
        "job_id": job_id,
        "status": "queued",
        "type": "video",
    }
