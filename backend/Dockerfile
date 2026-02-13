FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# ---- system deps (minimal & stable) ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ---- python deps ----
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---- app code ----
COPY . .

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV MEDIAPIPE_DISABLE_GPU=1
ENV CUDA_VISIBLE_DEVICES=-1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
