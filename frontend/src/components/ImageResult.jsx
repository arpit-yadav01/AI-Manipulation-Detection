function ImageResult({ result }) {
  if (!result) return null;

  const data = result.result;
  if (!data) return null;

  const verdict = data.final_verdict;

  return (
    <div style={{ marginTop: 30 }}>
      <h3>🖼 Image Results</h3>

      {/* ---------------- Scores ---------------- */}
      <p>
        <b>ELA Score:</b>{" "}
        {data.ela_score !== null ? data.ela_score : "N/A"}
      </p>

      <p>
        <b>ML Fake Probability:</b>{" "}
        {data.ml_fake_probability !== null
          ? Math.round(data.ml_fake_probability * 100) + "%"
          : "N/A"}
      </p>

      {/* ---------------- Verdict ---------------- */}
      {verdict && (
        <div style={{ padding: 15, border: "1px solid #ddd", marginTop: 10 }}>
          <p>
            <b>Verdict:</b>{" "}
            <span
              style={{
                padding: "4px 10px",
                borderRadius: 6,
                color: "white",
                background:
                  verdict.verdict === "LIKELY_FAKE"
                    ? "red"
                    : verdict.verdict === "LIKELY_REAL"
                    ? "green"
                    : "orange",
              }}
            >
              {verdict.verdict}
            </span>
          </p>

          <p>
            <b>Confidence:</b>{" "}
            {Math.round(verdict.confidence * 100)}%
          </p>
        </div>
      )}

      {data.prnu_score !== null && (
  <p>
    <b>PRNU Strength:</b> {data.prnu_score}
  </p>
)}

      {/* ---------------- Heatmap ---------------- */}
      {data.ela_heatmap && (
        <div style={{ marginTop: 20 }}>
          <h4>🔥 ELA / Grad-CAM Heatmap</h4>
          <img
            src={`http://localhost:8000${data.ela_heatmap}`}
            alt="Heatmap"
            style={{
              maxWidth: "100%",
              border: "1px solid #ccc",
              borderRadius: 6,
            }}
          />
        </div>
      )}

      {/* ---------------- EXIF ---------------- */}
      <div style={{ marginTop: 20 }}>
        <h4>📷 EXIF Metadata</h4>

        {data.exif && Object.keys(data.exif).length > 0 ? (
          <pre
            style={{
              maxHeight: 300,
              overflow: "auto",
              background: "#f6f6f6",
              padding: 10,
              fontSize: 12,
              borderRadius: 6,
            }}
          >
            {JSON.stringify(data.exif, null, 2)}
          </pre>
        ) : (
          <p style={{ color: "#888", fontSize: 13 }}>
            No EXIF metadata found (common for WhatsApp, screenshots, AI images)
          </p>
        )}
      </div>
    </div>
  );
}

export default ImageResult;
