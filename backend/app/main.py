# # from fastapi import FastAPI
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.staticfiles import StaticFiles

# # from app.api import image, result, video


# # def create_app():
# #     app = FastAPI(title="RealityCheck API")

# #     # -----------------------------a
# #     # CORS (Frontend Support)
# #     # -----------------------------
# #     app.add_middleware(
# #         CORSMiddleware,
# #         allow_origins=["http://localhost:5173"],
# #         allow_credentials=True,
# #         allow_methods=["*"],
# #         allow_headers=["*"],
# #     )

# #     # -----------------------------
# #     # API Routers
# #     # -----------------------------
# #     app.include_router(image.router, prefix="/api/image", tags=["image"])
# #     app.include_router(video.router, prefix="/api/video", tags=["video"])
# #     app.include_router(result.router, prefix="/api/result", tags=["result"])

# #     # -----------------------------
# #     # Static Files (Uploaded media)
# #     # -----------------------------
# #     app.mount(
# #         "/files",
# #         StaticFiles(directory="/app/datasets/uploads"),
# #         name="files"
# #     )

# #     # -----------------------------
# #     # Health Check
# #     # -----------------------------
# #     @app.get("/health")
# #     def health():
# #         return {"status": "ok"}

# #     return app


# # app = create_app()


# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles

# from app.api import image, result, video


# def create_app():
#     app = FastAPI(title="RealityCheck API")

#     # -----------------------------
#     # CORS (Frontend Support)
#     # -----------------------------
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=["http://localhost:5173"],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

#     # -----------------------------
#     # API Routers
#     # -----------------------------
#     app.include_router(image.router, prefix="/api/image", tags=["image"])
#     app.include_router(video.router, prefix="/api/video", tags=["video"])
#     app.include_router(result.router, prefix="/api/result", tags=["result"])

#     # -----------------------------
#     # Static Files (Uploaded media)
#     # -----------------------------
#     app.mount(
#         "/files",
#         StaticFiles(directory="/app/datasets/uploads"),
#         name="files",
#     )

#     # -----------------------------
#     # ✅ STATIC VIDEO FRAMES (STEP 10 FIX)
#     # -----------------------------
#     app.mount(
#         "/static/video_frames",
#         StaticFiles(directory="/app/datasets/video_frames"),
#         name="video_frames",
#     )

#     # -----------------------------
#     # Health Check
#     # -----------------------------
#     @app.get("/health")
#     def health():
#         return {"status": "ok"}

#     return app


# app = create_app()





from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import image, result, video

app = FastAPI(
    title="RealityCheck API",
    version="1.0.0"
)

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# API Routers
# -----------------------------
app.include_router(image.router, prefix="/api/image", tags=["image"])
app.include_router(video.router, prefix="/api/video", tags=["video"])
app.include_router(result.router, prefix="/api/result", tags=["result"])

# -----------------------------
# Static files
# -----------------------------
app.mount(
    "/files",
    StaticFiles(directory="/app/datasets/uploads", check_dir=False),
    name="files",
)

app.mount(
    "/static/video_frames",
    StaticFiles(directory="/app/datasets/video_frames", check_dir=False),
    name="video_frames",
)

# -----------------------------
# Health
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}
