from typing import Dict, Any, List


# ============================================================
# EXPERT-FACING DIFFUSION REPORT
# ============================================================

def _fmt(v, precision=4):
    if v is None:
        return "N/A"
    try:
        return round(float(v), precision)
    except Exception:
        return "N/A"


def generate_diffusion_expert_report(
    diffusion_evidence: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Converts diffusion evidence into a human-readable forensic report.

    🚫 NO verdicts
    🚫 NO thresholds
    🚫 NO classification
    ✅ Descriptive only
    """

    if not diffusion_evidence or not diffusion_evidence.get("available"):
        return {
            "available": False,
            "summary": "No diffusion-related forensic signals were available.",
            "sections": [],
        }

    sections: List[Dict[str, Any]] = []

    components = diffusion_evidence.get("components", {})

    # --------------------------------------------------------
    # 1️⃣ Noise Residual Analysis
    # --------------------------------------------------------
    nr = components.get("noise_residuals")
    if nr:
        sections.append({
            "title": "Diffusion Noise Residual Analysis",
            "description": (
                "Examines high-frequency residual patterns that remain after "
                "denoising. Diffusion-based generation often leaves structured "
                "residual energy that differs from natural camera noise."
            ),
            "observations": {
                "mean_residual_energy": _fmt(nr.get("mean_energy")),
                "std_residual_energy": _fmt(nr.get("std_energy")),
                "frames_analyzed": nr.get("frames_analyzed"),
            },
            "expert_note": (
                "Higher or unusually consistent residual energy across frames "
                "may indicate synthetic denoising processes, but this signal "
                "must be interpreted in context."
            ),
        })

    # --------------------------------------------------------
    # 2️⃣ Temporal Residual Stability
    # --------------------------------------------------------
    tr = components.get("temporal_residuals")
    if tr:
        sections.append({
            "title": "Temporal Residual Stability",
            "description": (
                "Analyzes how residual noise patterns evolve across time. "
                "Natural video exhibits stochastic variation, while diffusion "
                "models often maintain stable residual statistics."
            ),
            "observations": {
                "temporal_stability_score": _fmt(tr.get("stability_score")),
                "variance": _fmt(tr.get("variance")),
            },
            "expert_note": (
                "High temporal consistency in residuals can be characteristic "
                "of diffusion-based generation, though compression artifacts "
                "and post-processing may influence this signal."
            ),
        })

    # --------------------------------------------------------
    # 3️⃣ Cross-Signal Diffusion Correlation
    # --------------------------------------------------------
    cs = components.get("cross_signal_correlation")
    if cs:
        sections.append({
            "title": "Cross-Signal Diffusion Correlation",
            "description": (
                "Measures correlations between diffusion-sensitive signals "
                "(ELA, ML confidence, geometry drift, lighting drift). "
                "Synthetic pipelines often introduce correlated artifacts."
            ),
            "observations": {
                "ela_vs_ml": _fmt(cs.get("ela_vs_ml")),
                "ela_vs_geometry": _fmt(cs.get("ela_vs_geometry")),
                "ela_vs_lighting": _fmt(cs.get("ela_vs_lighting")),
                "ml_vs_geometry": _fmt(cs.get("ml_vs_geometry")),
                "ml_vs_lighting": _fmt(cs.get("ml_vs_lighting")),
                "mean_absolute_correlation": _fmt(
                    cs.get("mean_absolute_correlation")
                ),
                "num_correlations": cs.get("num_correlations"),
            },
            "expert_note": (
                "Consistent correlations across independent forensic signals "
                "may suggest a shared synthetic origin rather than natural "
                "capture artifacts."
            ),
        })

    # --------------------------------------------------------
    # 4️⃣ High-Level Expert Summary
    # --------------------------------------------------------
    summary = (
        "This report summarizes diffusion-related forensic observations "
        "without applying thresholds or classification. "
        "Signals should be interpreted jointly with temporal, identity, "
        "motion, and audio-visual analyses."
    )

    return {
        "available": True,
        "summary": summary,
        "sections": sections,
    }
