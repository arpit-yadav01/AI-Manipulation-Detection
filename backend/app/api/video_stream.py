from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.core.db import mongo
import os

router = APIRouter()

@router.get("/video/{job_id}")
def stream_video(job_id: str):
    record = mongo.results.find_one({"job_id": job_id})

    if not record:
        raise HTTPException(status_code=404, detail="Job not found")

    video_path = record.get("video_path")

    if not video_path or not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video file not found")

    return FileResponse(
        video_path,
        media_type="video/mp4"
    )
