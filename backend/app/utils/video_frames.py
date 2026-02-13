# import os
# import subprocess
# from pathlib import Path

# BASE_FRAMES_DIR = "/app/datasets/video_frames"


# def extract_frames(video_path: str, fps: int = 1) -> list[str]:
#     """
#     Extract frames from a video at fixed FPS.
#     Each video gets its own directory.
#     """

#     video_name = Path(video_path).stem
#     output_dir = os.path.join(BASE_FRAMES_DIR, video_name)

#     os.makedirs(output_dir, exist_ok=True)

#     output_pattern = os.path.join(output_dir, "frame_%04d.jpg")

#     cmd = [
#         "ffmpeg",
#         "-i", video_path,
#         "-vf", f"fps={fps}",
#         output_pattern,
#         "-y"
#     ]

#     subprocess.run(
#         cmd,
#         stdout=subprocess.DEVNULL,
#         stderr=subprocess.DEVNULL,
#         check=True
#     )

#     frames = sorted(
#         os.path.join(output_dir, f)
#         for f in os.listdir(output_dir)
#         if f.endswith(".jpg")
#     )

#     return frames



import cv2
import os
from pathlib import Path

BASE_FRAMES_DIR = "/app/datasets/video_frames"


def extract_frames(video_path: str, fps_sample: int = 1):
    """
    VIDEO_V2 — Extract frames with accurate timestamps.

    fps_sample = 1  → 1 frame per second
    fps_sample = 2  → 2 frames per second
    """

    video_name = Path(video_path).stem
    output_dir = os.path.join(BASE_FRAMES_DIR, video_name)
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        cap.release()
        raise RuntimeError("Invalid FPS detected")

    frame_interval = int(fps / fps_sample)

    frames = []
    frame_idx = 0
    saved_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % frame_interval == 0:
            timestamp = frame_idx / fps

            frame_name = f"frame_{saved_idx:04d}.jpg"
            frame_path = os.path.join(output_dir, frame_name)

            cv2.imwrite(frame_path, frame)

            frames.append({
                "path": frame_path,
                "timestamp": round(timestamp, 3),
            })

            saved_idx += 1

        frame_idx += 1

    cap.release()
    return frames
