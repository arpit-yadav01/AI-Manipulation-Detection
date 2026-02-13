import uuid
import os
import redis
from rq import Queue

from app.core.db import mongo
from app.workers.image_worker import process_image  # ✅ DIRECT IMPORT

UPLOAD_DIR = "/app/datasets/uploads/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

redis_conn = redis.Redis(host="redis", port=6379)
queue = Queue("default", connection=redis_conn)


async def enqueue_image_job(file):
    job_id = str(uuid.uuid4())

    ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, f"{job_id}{ext}")

    with open(file_path, "wb") as f:
        f.write(await file.read())

    mongo.results.insert_one({
        "job_id": job_id,
        "type": "image",
        "status": "queued"
    })

    # ✅ THIS IS THE FIX (NO STRING)
    queue.enqueue(
        process_image,
        job_id,
        file_path
    )

    return job_id
