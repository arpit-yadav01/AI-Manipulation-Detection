



# # ============================================================
# # 🔥 ABSOLUTE GPU / EGL HARD DISABLE (MUST BE FIRST)
# # ============================================================
# import os

# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
# os.environ["MEDIAPIPE_DISABLE_GPU"] = "1"
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
# os.environ["EGL_PLATFORM"] = "surfaceless"
# os.environ["DISPLAY"] = ""

# # 🔥 Prevent TensorFlow / MediaPipe GPU backends explicitly
# os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "false"
# os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# # ============================================================
# # SAFE IMPORTS (AFTER ENV LOCK)
# # ============================================================
# import traceback
# from app.core.db import mongo
# from app.video.final_fusion import fuse_video_signals

# # ============================================================
# # HARD SAFETY HELPERS
# # ============================================================

# def ensure_dict(obj, fallback: dict):
#     return obj if isinstance(obj, dict) else fallback


# def safe_signal(signal, verdict="insufficient_data"):
#     if isinstance(signal, dict):
#         return signal
#     return {"verdict": verdict, "confidence": 0.0}


# # ============================================================
# # MAIN VIDEO PROCESSOR (RQ WORKER)
# # ============================================================

# def process_video(job_id: str, video_path: str):

#     try:
#         # ----------------------------------------------------
#         # 🔥 LAZY IMPORTS (CPU-SAFE)
#         # ----------------------------------------------------
#         from app.utils.video_frames import extract_frames
#         from app.video.frame_analyzer import analyze_frame
#         from app.video.aggregator import aggregate_frames

#         from app.video.temporal.consistency import compute_temporal_stability
#         from app.video.deepfake.gan_artifacts import detect_gan_artifacts
#         from app.video.deepfake.motion import analyze_motion_consistency

#         from app.video.human_behavior.blink_detector import analyze_blink_consistency
#         from app.video.human_behavior.gaze_dynamics import analyze_gaze_dynamics
#         from app.video.human_behavior.micro_expression import analyze_micro_expression_consistency

#         from app.video.geometry.temporal_drift import compute_head_pose_drift

#         from app.video.audio_sync.audio_energy import extract_audio_energy
#         from app.video.audio_sync.lip_motion import extract_lip_motion
#         from app.video.audio_sync.av_sync import compute_av_sync

#         # PHASE 8
#         from app.video.audio_sync.speech_presence import detect_speech_presence
#         from app.video.audio_sync.lipsync_dominance import compute_lipsync_dominance

#         from app.video.video_ml.feature_aggregator import aggregate_video_features
#         from app.video.video_ml.video_classifier import classify_video

#         # DIFFUSION
#         from app.video.diffusion.noise_residual import analyze_diffusion_noise
#         from app.video.diffusion.temporal_residual import analyze_temporal_residual_stability
#         from app.video.evidence.evidence_accumulator import accumulate_evidence
#         from app.video.diffusion.expert_report import generate_diffusion_expert_report

#         # EXPLAINABILITY
#         from app.video.explainability.explanation_assembler import build_video_explanations

#         # TIMELINE
#         from app.video.timeline.frame_scoring import score_frame
#         from app.video.timeline.second_aggregation import aggregate_frames_to_seconds
#         from app.video.timeline.segment_detection import detect_manipulated_segments
#         from app.video.timeline.schema import build_video_timeline_schema

#         # ----------------------------------------------------
#         # FRAME EXTRACTION — 3 FPS (ANALYSIS ONLY)
#         # ----------------------------------------------------
#         frames = extract_frames(video_path, fps_sample=3)

#         frame_results = []
#         head_poses = []
#         lip_motion_curve = []

#         for idx, frame in enumerate(frames):
#             analysis = analyze_frame(frame["path"]) or {}

#             head_poses.append(analysis.get("geometry"))

#             lip = extract_lip_motion(frame["path"])
#             lip_motion_curve.append(lip["mouth_openness"] if lip else None)

#             frame_results.append({
#                 "frame_index": idx,
#                 "timestamp": frame["timestamp"],
#                 "path": frame["path"],
#                 **analysis,
#             })

#         # ----------------------------------------------------
#         # AUDIO + LIP SYNC
#         # ----------------------------------------------------
#         audio_energy = extract_audio_energy(video_path)
#         speech_signal = detect_speech_presence(audio_energy)

#         av_sync_signal = safe_signal(
#             compute_av_sync(
#                 audio_energy,
#                 [v for v in lip_motion_curve if v is not None],
#             )
#         )

#         lipsync_dominance = compute_lipsync_dominance(
#             speech_signal=speech_signal,
#             av_sync_signal=av_sync_signal,
#         )

#         severity_boost = lipsync_dominance.get("severity_boost", 0.0)

#         # ----------------------------------------------------
#         # TIMELINE
#         # ----------------------------------------------------
#         scored_frames = []

#         for f in frame_results:
#             base = score_frame(f)
#             boosted_score = min(1.0, base["score"] + severity_boost)

#             label = (
#                 "manipulated" if boosted_score >= 0.7
#                 else "suspicious" if boosted_score >= 0.4
#                 else "real"
#             )

#             scored_frames.append({
#                 "timestamp": f["timestamp"],
#                 "score": round(boosted_score, 3),
#                 "label": label,
#             })

#         second_scores = aggregate_frames_to_seconds(scored_frames, frames_per_second=3)
#         segments = detect_manipulated_segments(second_scores)

#         timeline = build_video_timeline_schema(
#             frames=scored_frames,
#             seconds=second_scores,
#             segments=segments,
#         )

#         # ----------------------------------------------------
#         # VIDEO-LEVEL AGGREGATION
#         # ----------------------------------------------------
#         aggregated = ensure_dict(
#             aggregate_frames(frame_results),
#             {"avg_fake_probability": 0.0, "frames_analyzed": len(frame_results)}
#         )

#         frame_stats = ensure_dict(
#             aggregate_video_features(frame_results),
#             {"avg_ml_fake_prob": 0.0, "std_ml_fake_prob": 1.0}
#         )

#         temporal_signal = safe_signal(compute_temporal_stability(frame_results))
#         gan_signal = safe_signal(detect_gan_artifacts([f["path"] for f in frame_results]))
#         motion_signal = safe_signal(analyze_motion_consistency([f["path"] for f in frame_results]))
#         geometry_drift_signal = safe_signal(compute_head_pose_drift(head_poses))

#         video_ml_signal = safe_signal(
#             classify_video(
#                 frame_stats=frame_stats,
#                 identity_stats={},
#                 geometry_stats=geometry_drift_signal,
#                 audio_sync_stats=av_sync_signal,
#             )
#         )

#         blink_signal = safe_signal(analyze_blink_consistency(frame_results))
#         gaze_signal = safe_signal(analyze_gaze_dynamics(frame_results))
#         micro_expression_signal = safe_signal(analyze_micro_expression_consistency(frame_results))

#         diffusion_noise = analyze_diffusion_noise([f["path"] for f in frame_results])
#         diffusion_temporal = analyze_temporal_residual_stability([f["path"] for f in frame_results])

#         diffusion_evidence = {
#             "available": bool(diffusion_noise and diffusion_noise.get("available")),
#             "components": {
#                 "noise_residuals": diffusion_noise,
#                 "temporal_residuals": diffusion_temporal,
#             },
#         }

#         evidence_summary = accumulate_evidence(
#             diffusion_evidence=diffusion_evidence,
#             temporal_signal=temporal_signal,
#             motion_signal=motion_signal,
#             gan_signal=gan_signal,
#             av_sync_signal=av_sync_signal,
#         )

#         expert_report = generate_diffusion_expert_report(diffusion_evidence)

#         final_verdict = fuse_video_signals(
#             avg_fake_probability=aggregated["avg_fake_probability"],
#             frames_analyzed=aggregated["frames_analyzed"],
#             temporal_signal=temporal_signal,
#             motion_signal=motion_signal,
#             gan_signal=gan_signal,
#             video_ml_signal=video_ml_signal,
#             blink_signal=blink_signal,
#             gaze_signal=gaze_signal,
#             micro_expression_signal=micro_expression_signal,
#         )
        

#         explanations = build_video_explanations(
#             temporal_signal=temporal_signal,
#             motion_signal=motion_signal,
#             identity_signal=None,
#             diffusion_evidence=diffusion_evidence,
#             frame_results=frame_results,
#             final_confidence=final_verdict.get("confidence"),
#         )

#         # ----------------------------------------------------
#         # SAVE RESULT
#         # ----------------------------------------------------
#         mongo.results.update_one(
#             {"job_id": job_id},
#             {
#                 "$set": {
#                     "status": "done",
#                     "result": {
#                         "type": "video",
#                         "final_verdict": final_verdict,
#                         "evidence_summary": evidence_summary,
#                         "expert_report": expert_report,
#                         "explanations": explanations,
#                         "timeline": timeline,
#                         "lipsync_dominance": lipsync_dominance,
#                     },
#                 }
#             },
#             upsert=True,
#         )

#     except Exception as e:
#         mongo.results.update_one(
#             {"job_id": job_id},
#             {
#                 "$set": {
#                     "status": "error",
#                     "error": str(e),
#                     "traceback": traceback.format_exc(),
#                 }
#             },
#             upsert=True,
#         )



# ============================================================
# 🔥 ABSOLUTE GPU / EGL HARD DISABLE (MUST BE FIRST)
# ============================================================
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["MEDIAPIPE_DISABLE_GPU"] = "1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["EGL_PLATFORM"] = "surfaceless"
os.environ["DISPLAY"] = ""
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "false"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# ============================================================
# SAFE IMPORTS
# ============================================================
import traceback
from app.core.db import mongo
from app.video.final_fusion import fuse_video_signals


# ============================================================
# SAFETY HELPERS
# ============================================================

def ensure_dict(obj, fallback: dict):
    return obj if isinstance(obj, dict) else fallback


def safe_signal(signal, verdict="insufficient_data"):
    if isinstance(signal, dict):
        return signal
    return {"verdict": verdict}


# ============================================================
# MAIN VIDEO PROCESSOR
# ============================================================

def process_video(job_id: str, video_path: str):

    try:
        # ----------------------------------------------------
        # LAZY IMPORTS
        # ----------------------------------------------------
        from app.utils.video_frames import extract_frames
        from app.video.frame_analyzer import analyze_frame
        from app.video.aggregator import aggregate_frames

        from app.video.temporal.consistency import compute_temporal_stability
        from app.video.deepfake.motion import analyze_motion_consistency
        from app.video.deepfake.gan_artifacts import detect_gan_artifacts
        from app.video.deepfake.identity import compute_identity_consistency

        from app.video.geometry.temporal_drift import compute_head_pose_drift

        from app.video.human_behavior.blink_detector import analyze_blink_consistency
        from app.video.human_behavior.gaze_dynamics import analyze_gaze_dynamics
        from app.video.human_behavior.micro_expression import analyze_micro_expression_consistency

        from app.video.audio_sync.audio_energy import extract_audio_energy
        from app.video.audio_sync.lip_motion import extract_lip_motion
        from app.video.audio_sync.av_sync import compute_av_sync
        from app.video.audio_sync.speech_presence import detect_speech_presence
        from app.video.audio_sync.lipsync_dominance import compute_lipsync_dominance

        from app.video.video_ml.feature_aggregator import aggregate_video_features
        from app.video.video_ml.video_classifier import classify_video

        from app.video.diffusion.noise_residual import analyze_diffusion_noise
        from app.video.diffusion.temporal_residual import analyze_temporal_residual_stability
        from app.video.evidence.evidence_accumulator import accumulate_evidence
        from app.video.diffusion.expert_report import generate_diffusion_expert_report

        from app.video.explainability.explanation_assembler import build_video_explanations

        from app.video.timeline.frame_scoring import score_frame
        from app.video.timeline.second_aggregation import aggregate_frames_to_seconds
        from app.video.timeline.segment_detection import detect_manipulated_segments
        from app.video.timeline.schema import build_video_timeline_schema

        from app.video.summarizers.temporal_motion_summary import (
            summarize_temporal,
            summarize_motion,
        )

        from app.video.summarizers.identity_geometry_summary import (
            summarize_identity,
            summarize_geometry,
        )

        from app.video.summarizers.av_sync_summary import summarize_av_sync

        # ----------------------------------------------------
        # FRAME EXTRACTION
        # ----------------------------------------------------
        frames = extract_frames(video_path, fps_sample=3)

        frame_results = []
        head_poses = []
        lip_motion_curve = []

        for idx, frame in enumerate(frames):
            analysis = analyze_frame(frame["path"]) or {}

            head_poses.append(analysis.get("geometry"))

            lip = extract_lip_motion(frame["path"])
            lip_motion_curve.append(lip["mouth_openness"] if lip else None)

            frame_results.append({
                "frame_index": idx,
                "timestamp": frame["timestamp"],
                "path": frame["path"],
                **analysis,
            })

        # ----------------------------------------------------
        # AUDIO + LIP SYNC
        # ----------------------------------------------------
        audio_energy = extract_audio_energy(video_path)
        speech_signal = detect_speech_presence(audio_energy)

        av_sync_signal = safe_signal(
            compute_av_sync(
                audio_energy,
                [v for v in lip_motion_curve if v is not None],
            )
        )

        lipsync_dominance = compute_lipsync_dominance(
            speech_signal=speech_signal,
            av_sync_signal=av_sync_signal,
        )

        av_sync_anomaly = summarize_av_sync(
            av_sync_signal,
            speech_signal,
        )

        severity_boost = lipsync_dominance.get("severity_boost", 0.0)

        # ----------------------------------------------------
        # TIMELINE BUILD
        # ----------------------------------------------------
        scored_frames = []

        for f in frame_results:
            base = score_frame(f)
            boosted_score = min(1.0, base["score"] + severity_boost)

            label = (
                "manipulated" if boosted_score >= 0.7
                else "suspicious" if boosted_score >= 0.4
                else "real"
            )

            scored_frames.append({
                "timestamp": f["timestamp"],
                "score": round(boosted_score, 3),
                "label": label,
            })

        second_scores = aggregate_frames_to_seconds(scored_frames, frames_per_second=3)
        segments = detect_manipulated_segments(second_scores)

        timeline = build_video_timeline_schema(
            frames=scored_frames,
            seconds=second_scores,
            segments=segments,
        )

        # ----------------------------------------------------
        # VIDEO-LEVEL AGGREGATION
        # ----------------------------------------------------
        aggregated = ensure_dict(
            aggregate_frames(frame_results),
            {"avg_fake_probability": 0.0, "frames_analyzed": len(frame_results)},
        )

        frames_count = aggregated["frames_analyzed"]

        frame_stats = ensure_dict(
            aggregate_video_features(frame_results),
            {"avg_ml_fake_prob": 0.0, "std_ml_fake_prob": 1.0},
        )

        # ----------------------------------------------------
        # CORE SIGNALS
        # ----------------------------------------------------
        temporal_signal = safe_signal(compute_temporal_stability(frame_results))
        motion_signal = safe_signal(analyze_motion_consistency([f["path"] for f in frame_results]))
        gan_signal = safe_signal(detect_gan_artifacts([f["path"] for f in frame_results]))
        identity_signal = safe_signal(compute_identity_consistency([f["path"] for f in frame_results]))
        geometry_signal = safe_signal(compute_head_pose_drift(head_poses))

        # ----------------------------------------------------
        # NORMALIZED ANOMALIES
        # ----------------------------------------------------
        temporal_anomaly = summarize_temporal(temporal_signal)
        motion_anomaly = summarize_motion(motion_signal)
        identity_anomaly = summarize_identity(identity_signal)
        geometry_anomaly = summarize_geometry(geometry_signal)

        # ----------------------------------------------------
        # 🔵 SECTION 4 — RELIABILITY WEIGHTS
        # ----------------------------------------------------
        temporal_reliability = 1.0 if frames_count >= 10 else 0.5
        motion_reliability = 1.0 if frames_count >= 10 else 0.5

        identity_reliability = 1.0 if identity_signal.get("mean_similarity") else 0.4
        geometry_reliability = 1.0 if geometry_signal.get("available") else 0.4

        gan_reliability = 1.0 if frames_count >= 10 else 0.6
        av_reliability = 1.0 if speech_signal.get("speech_present") else 0.3

        # ----------------------------------------------------
        # VIDEO ML
        # ----------------------------------------------------
        video_ml_signal = safe_signal(
            classify_video(
                frame_stats=frame_stats,
                identity_stats={},
                geometry_stats=geometry_signal,
                audio_sync_stats=av_sync_signal,
            )
        )

        blink_signal = safe_signal(analyze_blink_consistency(frame_results))
        gaze_signal = safe_signal(analyze_gaze_dynamics(frame_results))
        micro_expression_signal = safe_signal(analyze_micro_expression_consistency(frame_results))

        # ----------------------------------------------------
        # DIFFUSION EVIDENCE
        # ----------------------------------------------------
        diffusion_noise = analyze_diffusion_noise([f["path"] for f in frame_results])
        diffusion_temporal = analyze_temporal_residual_stability([f["path"] for f in frame_results])

        diffusion_evidence = {
            "available": bool(diffusion_noise and diffusion_noise.get("available")),
            "components": {
                "noise_residuals": diffusion_noise,
                "temporal_residuals": diffusion_temporal,
            },
        }

        evidence_summary = accumulate_evidence(
            diffusion_evidence=diffusion_evidence,
            temporal_signal=temporal_signal,
            motion_signal=motion_signal,
            gan_signal=gan_signal,
            av_sync_signal=av_sync_signal,
        )

        expert_report = generate_diffusion_expert_report(diffusion_evidence)

        # ----------------------------------------------------
        # FINAL FUSION (SECTION 4 ENABLED)
        # ----------------------------------------------------
        final_verdict = fuse_video_signals(
            avg_fake_probability=aggregated["avg_fake_probability"],
            frames_analyzed=frames_count,

            temporal_anomaly=temporal_anomaly,
            motion_anomaly=motion_anomaly,
            identity_anomaly=identity_anomaly,
            geometry_anomaly=geometry_anomaly,
            av_sync_anomaly=av_sync_anomaly,

            temporal_reliability=temporal_reliability,
            motion_reliability=motion_reliability,
            identity_reliability=identity_reliability,
            geometry_reliability=geometry_reliability,
            gan_reliability=gan_reliability,
            av_reliability=av_reliability,

            gan_signal=gan_signal,
            video_ml_signal=video_ml_signal,

            blink_signal=blink_signal,
            gaze_signal=gaze_signal,
            micro_expression_signal=micro_expression_signal,

            evidence_summary=evidence_summary,
            av_sync_signal=av_sync_signal,
       

        )

        explanations = build_video_explanations(
            temporal_signal=temporal_signal,
            motion_signal=motion_signal,
            identity_signal=identity_signal,
            diffusion_evidence=diffusion_evidence,
            frame_results=frame_results,
            final_confidence=final_verdict.get("confidence"),
        )

        # ----------------------------------------------------
        # SAVE RESULT
        # ----------------------------------------------------
        mongo.results.update_one(
            {"job_id": job_id},
            {
                "$set": {
                    "status": "done",
                    "result": {
                        "type": "video",
                        "final_verdict": final_verdict,
                        "evidence_summary": evidence_summary,
                        "expert_report": expert_report,
                        "explanations": explanations,
                        "timeline": timeline,
                        "lipsync_dominance": lipsync_dominance,
                        
                    },
                }
            },
            upsert=True,
        )

    except Exception as e:
        mongo.results.update_one(
            {"job_id": job_id},
            {
                "$set": {
                    "status": "error",
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                }
            },
            upsert=True,
        )
