import torch
import numpy as np
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import cv2

# --------------------------------------------------
# CPU ONLY
# --------------------------------------------------
DEVICE = torch.device("cpu")

_mtcnn = None
_resnet = None


def get_mtcnn():
    global _mtcnn
    if _mtcnn is None:
        _mtcnn = MTCNN(
            image_size=160,
            margin=20,
            min_face_size=40,
            thresholds=[0.6, 0.7, 0.7],
            device=DEVICE
        )
    return _mtcnn


def get_resnet():
    global _resnet
    if _resnet is None:
        _resnet = InceptionResnetV1(
            pretrained="vggface2"
        ).eval().to(DEVICE)
    return _resnet


def extract_face_embedding(frame_path: str):
    """
    Input: frame image path
    Output: 512-D embedding OR None
    SAFE: models loaded lazily inside worker
    """

    try:
        frame = cv2.imread(frame_path)
        if frame is None:
            return None

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)

        mtcnn = get_mtcnn()
        resnet = get_resnet()

        face = mtcnn(img)
        if face is None:
            return None

        with torch.no_grad():
            embedding = resnet(face.unsqueeze(0))

        return embedding.squeeze(0).cpu().numpy()

    except Exception:
        return None
