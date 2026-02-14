FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# ------------------------------------------------------------
# System dependencies (dlib + face_recognition required)
# ------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    gcc \
    g++ \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ------------------------------------------------------------
# Python dependencies
# ------------------------------------------------------------
# ---- python deps ----
COPY requirements.txt .

RUN pip install --upgrade pip==24.0 setuptools==69.5.1 wheel==0.43.0 && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir git+https://github.com/openai/CLIP.git


# ------------------------------------------------------------
# App code
# ------------------------------------------------------------
COPY . .

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV MEDIAPIPE_DISABLE_GPU=1
ENV CUDA_VISIBLE_DEVICES=-1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
