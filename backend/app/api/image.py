from fastapi import APIRouter, UploadFile, File
from app.services.image_queue import enqueue_image_job

router = APIRouter()


@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    job_id = await enqueue_image_job(file)
    return {
        "job_id": job_id,
        "status": "queued",
        "type": "image"
    }
