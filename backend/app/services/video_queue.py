
# # app/services/video_queue.py

# import uuid
# import os
# import redis
# from rq import Queue
# from fastapi import UploadFile
# from shutil import copyfileobj

# from app.core.db import mongo

# UPLOAD_DIR = "/app/datasets/uploads/videos"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# redis_conn = redis.Redis(host="redis", port=6379)
# queue = Queue("default", connection=redis_conn)


# def enqueue_video_job(file: UploadFile) -> str:
#     """
#     SAFE video enqueue:
#     - stream file to disk
#     - close UploadFile explicitly
#     - enqueue RQ job
#     """

#     job_id = str(uuid.uuid4())

#     ext = os.path.splitext(file.filename)[1]
#     file_path = os.path.join(UPLOAD_DIR, f"{job_id}{ext}")

#     try:
#         # ✅ STREAM COPY (NO .read())
#         with open(file_path, "wb") as out_file:
#             copyfileobj(file.file, out_file)

#     finally:
#         # ✅ CRITICAL: close UploadFile
#         file.file.close()

#     # ✅ Insert initial DB record
#     mongo.results.insert_one({
#         "job_id": job_id,
#         "type": "video",
#         "status": "queued",
#          "video_path": file_path,
#     })

#     # ✅ Enqueue worker (string import is correct)
#     queue.enqueue(
#         "app.workers.video_worker.process_video",
#         job_id,
#         file_path,
#         job_timeout="2h"
#     )

#     return job_id



# app/services/video_queue.py

import uuid
import os
import redis
from rq import Queue
from fastapi import UploadFile
from shutil import copyfileobj

from app.core.db import mongo

UPLOAD_DIR = "/app/datasets/uploads/videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

redis_conn = redis.Redis(host="redis", port=6379)
queue = Queue("default", connection=redis_conn)


def enqueue_video_job(file: UploadFile) -> str:
    """
    SAFE video enqueue:
    - stream file to disk
    - close UploadFile explicitly
    - enqueue RQ job
    """

    job_id = str(uuid.uuid4())

    ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, f"{job_id}{ext}")

    try:
        # ✅ STREAM COPY (NO .read())
        with open(file_path, "wb") as out_file:
            copyfileobj(file.file, out_file)

    finally:
        # ✅ CRITICAL: close UploadFile
        file.file.close()

    # ✅ Insert initial DB record
    mongo.results.insert_one({
        "job_id": job_id,
        "type": "video",
        "status": "queued",
         "video_path": file_path,
    })

    # ✅ Enqueue worker (string import is correct)
    
# app/services/video_queue.py

import uuid
import os
import redis
from rq import Queue
from fastapi import UploadFile
from shutil import copyfileobj

from app.core.db import mongo

UPLOAD_DIR = "/app/datasets/uploads/videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

redis_conn = redis.Redis(host="redis", port=6379)
queue = Queue("default", connection=redis_conn)


def enqueue_video_job(file: UploadFile) -> str:
    """
    SAFE video enqueue:
    - stream file to disk
    - close UploadFile explicitly
    - enqueue RQ job
    """

    job_id = str(uuid.uuid4())

    ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, f"{job_id}{ext}")

    try:
        # ✅ STREAM COPY (NO .read())
        with open(file_path, "wb") as out_file:
            copyfileobj(file.file, out_file)

    finally:
        # ✅ CRITICAL: close UploadFile
        file.file.close()

    # ✅ Insert initial DB record
    mongo.results.insert_one({
        "job_id": job_id,
        "type": "video",
        "status": "queued",
         "video_path": file_path,
    })

    # ✅ Enqueue worker (string import is correct)
    queue.enqueue(
        "app.workers.video_worker.process_video",
        job_id,
        file_path,
        job_timeout="2h"
    )

    return job_id


    return job_id
