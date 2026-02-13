from typing import Dict, Any, Optional
import numpy as np


# ============================================================
# DIFFUSION EVIDENCE ACCUMULATOR (RESEARCH-GRADE, NO DECISIONS)
# ============================================================

def _safe_float(v) -> Optional[float]:
    try:
        if v is None:
            return None
        return float(v)
    except Exception:
        return None


def _safe_mean(values):
    vals = [float(v) for v in values if isinstance(v, (int, float))]
    if not vals:
        return None
    return float(np.mean(vals))


def accumulate_diffusion_evidence(
    *,
    noise_residual_signal: Optional[Dict[str, Any]],
    temporal_residual_signal: Optional[Dict[str, Any]],
    cross_signal_correlation: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Collects ALL diffusion-related forensic signals into ONE container.

    🚫 NO thresholds
    🚫 NO verdicts
    🚫 NO weighting
    ✅ Evidence only
    """

    evidence = {
        "available": False,
        "components": {},
        "summary": {},
    }

    # --------------------------------------------------------
    # 1️⃣ Noise Residual Evidence
    # --------------------------------------------------------
    if noise_residual_signal and noise_residual_signal.get("available"):
        evidence["components"]["noise_residuals"] = {
            "mean_energy": _safe_float(
                noise_residual_signal.get("mean_residual_energy")
            ),
            "std_energy": _safe_float(
                noise_residual_signal.get("std_residual_energy")
            ),
            "frames_analyzed": noise_residual_signal.get(
                "frames_analyzed"
            ),
        }

    # --------------------------------------------------------
    # 2️⃣ Temporal Residual Stability
    # --------------------------------------------------------
    if temporal_residual_signal and temporal_residual_signal.get("available"):
        evidence["components"]["temporal_residuals"] = {
            "stability_score": _safe_float(
                temporal_residual_signal.get("temporal_stability_score")
            ),
            "variance": _safe_float(
                temporal_residual_signal.get("variance")
            ),
        }

    # --------------------------------------------------------
    # 3️⃣ Cross-Signal Correlation
    # --------------------------------------------------------
    if cross_signal_correlation and cross_signal_correlation.get("available"):
        corr = cross_signal_correlation.get("correlations", {})
        evidence["components"]["cross_signal_correlation"] = {
            "ela_vs_ml": _safe_float(corr.get("ela_vs_ml")),
            "ela_vs_geometry": _safe_float(corr.get("ela_vs_geometry")),
            "ela_vs_lighting": _safe_float(corr.get("ela_vs_lighting")),
            "ml_vs_geometry": _safe_float(corr.get("ml_vs_geometry")),
            "ml_vs_lighting": _safe_float(corr.get("ml_vs_lighting")),
            "mean_absolute_correlation": _safe_float(
                corr.get("mean_absolute_correlation")
            ),
            "num_correlations": corr.get("num_correlations"),
        }

    # --------------------------------------------------------
    # 4️⃣ High-Level Summary (DESCRIPTIVE ONLY)
    # --------------------------------------------------------
    summary_metrics = []

    # Collect representative scalar signals for inspection
    nr = evidence["components"].get("noise_residuals")
    if nr:
        summary_metrics.append(nr.get("mean_energy"))

    tr = evidence["components"].get("temporal_residuals")
    if tr:
        summary_metrics.append(tr.get("stability_score"))

    cs = evidence["components"].get("cross_signal_correlation")
    if cs:
        summary_metrics.append(cs.get("mean_absolute_correlation"))

    evidence["summary"] = {
        "num_components": len(evidence["components"]),
        "mean_signal_level": _safe_mean(summary_metrics),
        "note": (
            "Descriptive aggregation only. "
            "No thresholds or verdicts applied."
        ),
    }

    evidence["available"] = len(evidence["components"]) > 0
    return evidence
