import os
import subprocess

FRAMES_DIR = "/app/datasets/video_frames"


def extract_frames(video_path: str, fps: int = 1) -> list[str]:
    """
    Extract frames from video at fixed FPS.
    """

    # 1️⃣ Create directory if not exists
    os.makedirs(FRAMES_DIR, exist_ok=True)

    # 2️⃣ Output naming pattern
    output_pattern = os.path.join(
        FRAMES_DIR,
        os.path.basename(video_path) + "_%04d.jpg"
    )

    # 3️⃣ FFmpeg command
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"fps={fps}",
        output_pattern,
        "-y"
    ]

    # 4️⃣ Run FFmpeg
    subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )

    # 5️⃣ Collect frames
    frames = sorted([
        os.path.join(FRAMES_DIR, f)
        for f in os.listdir(FRAMES_DIR)
        if f.startswith(os.path.basename(video_path))
    ])

    return frames
