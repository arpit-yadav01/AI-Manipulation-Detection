import os
import cv2
import numpy as np

# --------------------------------------------------
# DO NOT IMPORT MEDIAPIPE AT MODULE LEVEL
# --------------------------------------------------

# Stable landmark indices
LANDMARK_IDS = {
    "nose": 1,
    "chin": 152,
    "left_eye": 33,
    "right_eye": 263,
    "left_mouth": 61,
    "right_mouth": 291,
}

# Generic 3D face model (mm)
MODEL_POINTS = np.array([
    (0.0, 0.0, 0.0),       # nose
    (0.0, -63.6, -12.5),  # chin
    (-43.3, 32.7, -26.0), # left eye
    (43.3, 32.7, -26.0),  # right eye
    (-28.9, -28.9, -24.1),
    (28.9, -28.9, -24.1),
])


def estimate_head_pose(image_path: str):
    """
    Returns yaw / pitch / roll (degrees) or None
    SAFE: MediaPipe loaded ONLY inside worker execution.
    """

    # 🔒 HARD SAFETY (inside function)
    os.environ["MEDIAPIPE_DISABLE_GPU"] = "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    os.environ["EGL_PLATFORM"] = "surfaceless"

    import mediapipe as mp  # 🔥 LAZY IMPORT (CRITICAL)

    mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    img = cv2.imread(image_path)
    if img is None:
        return None

    h, w = img.shape[:2]
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = mp_face_mesh.process(rgb)
    if not result.multi_face_landmarks:
        return None

    face = result.multi_face_landmarks[0]

    image_points = np.array([
        (face.landmark[LANDMARK_IDS["nose"]].x * w,
         face.landmark[LANDMARK_IDS["nose"]].y * h),

        (face.landmark[LANDMARK_IDS["chin"]].x * w,
         face.landmark[LANDMARK_IDS["chin"]].y * h),

        (face.landmark[LANDMARK_IDS["left_eye"]].x * w,
         face.landmark[LANDMARK_IDS["left_eye"]].y * h),

        (face.landmark[LANDMARK_IDS["right_eye"]].x * w,
         face.landmark[LANDMARK_IDS["right_eye"]].y * h),

        (face.landmark[LANDMARK_IDS["left_mouth"]].x * w,
         face.landmark[LANDMARK_IDS["left_mouth"]].y * h),

        (face.landmark[LANDMARK_IDS["right_mouth"]].x * w,
         face.landmark[LANDMARK_IDS["right_mouth"]].y * h),
    ], dtype="double")

    focal_length = w
    center = (w / 2, h / 2)

    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ])

    dist_coeffs = np.zeros((4, 1))

    success, rvec, _ = cv2.solvePnP(
        MODEL_POINTS,
        image_points,
        camera_matrix,
        dist_coeffs,
        flags=cv2.SOLVEPNP_ITERATIVE
    )

    if not success:
        return None

    rmat, _ = cv2.Rodrigues(rvec)

    pitch = np.arctan2(
        -rmat[2][0],
        np.sqrt(rmat[2][1] ** 2 + rmat[2][2] ** 2)
    ) * 180 / np.pi

    yaw = np.arctan2(rmat[1][0], rmat[0][0]) * 180 / np.pi
    roll = np.arctan2(rmat[2][1], rmat[2][2]) * 180 / np.pi

    return {
        "yaw": round(float(yaw), 2),
        "pitch": round(float(pitch), 2),
        "roll": round(float(roll), 2),
    }
