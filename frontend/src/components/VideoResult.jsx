

// import { useRef, useState } from "react";
// import VerdictBadge from "./VerdictBadge";

// /* ===== Time Formatter (PHASE 5) ===== */
// function formatTime(sec) {
//   const m = Math.floor(sec / 60);
//   const s = (sec % 60).toFixed(1);
//   return `${m.toString().padStart(2, "0")}:${s.padStart(4, "0")}`;
// }

// function VideoResult({ result }) {
//   const [selectedFrame, setSelectedFrame] = useState(null);
//   const [currentTime, setCurrentTime] = useState(0);
//   const [duration, setDuration] = useState(0);
//   const videoRef = useRef(null);

//   if (!result) {
//     return <p>⏳ Processing video…</p>;
//   }

//   const video = result.result ?? result;
//   const verdict = video.final_verdict;
//   const frames = video.explanations?.frames || [];
//   const signals = video.signals || {};
//   const aiSegments = video.ai_segments || [];

//   const fakeConfidence = verdict?.confidence ?? 0;
//   const realConfidence = Math.max(0, 1 - fakeConfidence);

//   /* ===== AI check using REAL timestamps (PHASE 6) ===== */
//   const isAI = aiSegments.some(
//     (seg) => currentTime >= seg.start && currentTime <= seg.end
//   );

//   function isAISec(sec) {
//     return aiSegments.some(
//       (seg) => sec >= seg.start && sec <= seg.end
//     );
//   }

//   function getSegmentForSec(sec) {
//     return aiSegments.find(
//       (seg) => sec >= seg.start && sec <= seg.end
//     );
//   }

//   function jumpTo(sec) {
//     if (videoRef.current) {
//       videoRef.current.currentTime = sec;
//       videoRef.current.play();
//     }
//   }

//   const totalSeconds = Math.ceil(duration);

//   return (
//     <div style={{ marginTop: 30 }}>
//       <h3>🎬 Video Results</h3>

//       {/* ===== VIDEO PLAYER WITH OVERLAY ===== */}
//       <div style={{ position: "relative", marginBottom: 15 }}>
//         <video
//           ref={videoRef}
//           controls
//           style={videoStyle}
//           onLoadedMetadata={(e) => setDuration(e.target.duration)}
//           onTimeUpdate={(e) => setCurrentTime(e.target.currentTime)}
//         >
//           <source src={video.video_url} type="video/mp4" />
//         </video>

//         <div
//           style={{
//             position: "absolute",
//             top: 12,
//             left: 12,
//             padding: "6px 12px",
//             borderRadius: 6,
//             fontWeight: 600,
//             color: "white",
//             background: isAI ? "#e74c3c" : "#2ecc71",
//           }}
//         >
//           {isAI
//             ? "🔴 AI MANIPULATION DETECTED"
//             : "🟢 VERIFIED REAL CONTENT"}
//         </div>
//       </div>

//       {/* ===== TIMELINE BAR (PHASE 3 + 5 + 6 🔥) ===== */}
//       {totalSeconds > 0 && (
//         <div style={card}>
//           <h4>📊 AI / Real Timeline</h4>

//           <div style={timelineBar}>
//             {Array.from({ length: totalSeconds }).map((_, sec) => {
//               const ai = isAISec(sec);
//               const active =
//                 currentTime >= sec && currentTime < sec + 1;

//               const seg = getSegmentForSec(sec);
//               const tooltip = seg
//                 ? `AI detected: ${formatTime(
//                     seg.start
//                   )} – ${formatTime(seg.end)}`
//                 : `Real content: ${formatTime(sec)}`;

//               return (
//                 <div
//                   key={sec}
//                   title={tooltip}
//                   onClick={() => jumpTo(sec)}
//                   style={{
//                     ...timeBlock,
//                     background: ai ? "#e74c3c" : "#2ecc71",
//                     opacity: active ? 1 : 0.5,
//                     outline: active
//                       ? "2px solid #000"
//                       : "none",
//                   }}
//                 />
//               );
//             })}
//           </div>

//           <div style={{ marginTop: 8, fontSize: 14 }}>
//             <span style={{ color: "#2ecc71" }}>🟢 Real</span>{" "}
//             &nbsp;|&nbsp;
//             <span style={{ color: "#e74c3c" }}>🔴 AI</span>{" "}
//             &nbsp;• Click to jump
//           </div>

//           {/* ===== AI SEGMENT LIST (PHASE 5 BONUS) ===== */}
//           {aiSegments.length > 0 && (
//             <div style={{ marginTop: 8, fontSize: 14 }}>
//               <b>AI detected at:</b>
//               <ul>
//                 {aiSegments.map((seg, i) => (
//                   <li key={i}>
//                     {formatTime(seg.start)} –{" "}
//                     {formatTime(seg.end)}
//                   </li>
//                 ))}
//               </ul>
//             </div>
//           )}
//         </div>
//       )}

//       {/* ===== Verdict Summary ===== */}
//       {verdict && (
//         <div style={card}>
//           <p>
//             <b>Verdict:</b>{" "}
//             <VerdictBadge verdict={verdict.verdict} />
//           </p>
//           <p>
//             <b>Confidence:</b>{" "}
//             {Math.round(realConfidence * 100)}% Real
//           </p>
//           <p>
//             <b>Frames analyzed:</b>{" "}
//             {verdict.frames_analyzed}
//           </p>
//         </div>
//       )}

//       {/* ===== Frame Timeline ===== */}
//       {frames.length > 0 && (
//         <div>
//           <h4>🧵 Suspicious Frames</h4>
//           <div style={frameTimeline}>
//             {frames.map((frame, idx) => {
//               const prob = frame.ml_fake_probability || 0;
//               const color =
//                 prob > 0.4
//                   ? "#e74c3c"
//                   : prob > 0.15
//                   ? "#f1c40f"
//                   : "#2ecc71";

//               return (
//                 <img
//                   key={idx}
//                   src={frame.frame_path}
//                   onClick={() => setSelectedFrame(frame)}
//                   alt=""
//                   style={{
//                     ...thumb,
//                     borderColor: color,
//                   }}
//                 />
//               );
//             })}
//           </div>
//         </div>
//       )}

//       {/* ===== Frame Detail ===== */}
//       {selectedFrame && (
//         <div style={card}>
//           <h4>🖼 Frame Detail</h4>
//           <img
//             src={selectedFrame.frame_path}
//             alt="selected-frame"
//             style={frameDetailStyle}
//           />
//           <p>
//             <b>ML Fake Probability:</b>{" "}
//             {(selectedFrame.ml_fake_probability * 100).toFixed(
//               2
//             )}
//             %
//           </p>
//           <p>
//             <b>Explanation:</b>{" "}
//             {selectedFrame.explanation}
//           </p>
//         </div>
//       )}

//       {/* ===== Signal Breakdown ===== */}
//       <div style={card}>
//         <h4>📊 Signal Breakdown</h4>
//         <SignalRow
//           label="Temporal Consistency"
//           value={signals.temporal?.verdict}
//           ok={signals.temporal?.verdict === "stable"}
//         />
//         <SignalRow
//           label="Motion Pattern"
//           value={signals.motion?.verdict}
//           ok={signals.motion?.verdict === "natural_motion"}
//         />
//         <SignalRow
//           label="GAN Artifacts"
//           value={signals.gan?.verdict}
//           ok={false}
//           note="Weak signal"
//         />
//       </div>
//     </div>
//   );
// }

// function SignalRow({ label, value, ok, note }) {
//   return (
//     <p>
//       <b>{label}:</b>{" "}
//       <span style={{ color: ok ? "green" : "orange" }}>
//         {value || "N/A"}
//       </span>
//       {note && (
//         <span style={{ color: "#777" }}> ({note})</span>
//       )}
//     </p>
//   );
// }

// /* ===== STYLES ===== */

// const card = {
//   padding: 15,
//   border: "1px solid #ddd",
//   borderRadius: 6,
//   marginBottom: 20,
// };

// const timelineBar = {
//   display: "flex",
//   gap: 2,
//   overflowX: "auto",
// };

// const timeBlock = {
//   width: 14,
//   height: 20,
//   cursor: "pointer",
//   borderRadius: 2,
// };

// const frameTimeline = {
//   display: "flex",
//   gap: 10,
//   overflowX: "auto",
//   paddingBottom: 10,
// };

// const thumb = {
//   width: 120,
//   height: 80,
//   objectFit: "cover",
//   border: "3px solid transparent",
//   borderRadius: 6,
//   cursor: "pointer",
// };

// const videoStyle = {
//   width: "70%",
//   maxWidth: 400,
//   borderRadius: 8,
//   display: "block",
//   margin: "0 auto",
// };

// const frameDetailStyle = {
//   width: "50%",
//   maxWidth: 300,
//   borderRadius: 6,
//   display: "block",
//   margin: "10px auto",
//   border: "1px solid #e5e7eb",
// };

// export default VideoResult;




import { useRef, useState, useEffect } from "react";
import VerdictBadge from "./VerdictBadge";

/* ===== Time Formatter ===== */
function formatTime(sec) {
  const m = Math.floor(sec / 60);
  const s = (sec % 60).toFixed(1);
  return `${m.toString().padStart(2, "0")}:${s.padStart(4, "0")}`;
}

function VideoResult({ result }) {
  const videoRef = useRef(null);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [selectedFrame, setSelectedFrame] = useState(null);
  const [videoError, setVideoError] = useState(null);
  const [videoLoading, setVideoLoading] = useState(true);

  if (!result) return <p>⏳ Processing video…</p>;

  const video = result.result ?? result;
  const verdict = video.final_verdict;
  const timeline = video.timeline;
  const frames = video.explanations?.frames || [];
  const signals = video.signals || {};

  // Debug log for video URL
  console.log("Video URL:", video.video_url);

  // Backward compatibility: if timeline doesn't exist, use old structure
  const secondLevel = timeline?.second_level || [];
  const segments = timeline?.segments || [];
  const aiSegments = video.ai_segments || [];

  function jumpTo(sec) {
    if (videoRef.current) {
      videoRef.current.currentTime = sec;
      videoRef.current.play();
    }
  }

  function segmentAtSecond(sec) {
    if (segments.length > 0) {
      return segments.find(s => sec >= s.start && sec <= s.end);
    }
    // Fallback to old aiSegments structure
    return aiSegments.find(seg => sec >= seg.start && sec <= seg.end);
  }

  function isAISec(sec) {
    return !!segmentAtSecond(sec);
  }

  const totalSeconds = Math.ceil(duration);
  const currentSegment = segmentAtSecond(Math.floor(currentTime));
  const isManipulated = !!currentSegment;

  // Handle video errors
  const handleVideoError = (e) => {
    console.error("Video error:", e);
    setVideoError("Failed to load video. Please check the video URL.");
    setVideoLoading(false);
  };

  const handleVideoLoad = () => {
    setVideoLoading(false);
    setVideoError(null);
  };

  return (
    <div style={{ marginTop: 30 }}>
      <h3>🎬 Video Results</h3>

      {/* ===== VIDEO PLAYER WITH OVERLAY ===== */}
      <div style={{ position: "relative", marginBottom: 15 }}>
        {videoError ? (
          <div style={errorContainer}>
            <p style={{ color: "#e74c3c" }}>❌ {videoError}</p>
            <p>Video URL: {video.video_url}</p>
          </div>
        ) : (
          <>
            {videoLoading && <p style={{ textAlign: "center" }}>📹 Loading video...</p>}
            <video
              ref={videoRef}
              controls
              style={videoStyle}
              onLoadedMetadata={(e) => {
                setDuration(e.target.duration);
                handleVideoLoad();
              }}
              onTimeUpdate={(e) => setCurrentTime(e.target.currentTime)}
              onError={handleVideoError}
              onCanPlay={handleVideoLoad}
              preload="metadata"
            >
              <source src={video.video_url} type="video/mp4" />
              <source src={video.video_url} type="video/webm" />
              Your browser does not support the video tag.
            </video>

            {/* Live overlay */}
            <div
              style={{
                position: "absolute",
                top: 12,
                left: 12,
                padding: "6px 12px",
                borderRadius: 6,
                fontWeight: 600,
                color: "white",
                background: isManipulated ? "#e74c3c" : "#2ecc71",
                zIndex: 10,
              }}
            >
              {isManipulated
                ? "🔴 MANIPULATION DETECTED"
                : "🟢 NO MANIPULATION DETECTED"}
            </div>
          </>
        )}
      </div>

      {/* ===== TIMELINE BAR ===== */}
      {totalSeconds > 0 && (
        <div style={card}>
          <h4>📊 AI / Real Timeline</h4>

          <div style={timelineBar}>
            {Array.from({ length: totalSeconds }).map((_, sec) => {
              const manipulated = isAISec(sec);
              const active = currentTime >= sec && currentTime < sec + 1;
              
              // Try to get detailed label from timeline structure
              const timelineEntry = secondLevel.find(s => s.second === sec);
              const label = timelineEntry?.label || (manipulated ? "manipulated" : "real");
              
              const color = 
                label === "manipulated" ? "#e74c3c" :
                label === "suspicious" ? "#f1c40f" :
                "#2ecc71";

              const segment = segmentAtSecond(sec);
              const tooltip = segment
                ? `Manipulation: ${formatTime(segment.start)} – ${formatTime(segment.end)}`
                : `Real content: ${formatTime(sec)}`;

              return (
                <div
                  key={sec}
                  title={tooltip}
                  onClick={() => jumpTo(sec)}
                  style={{
                    ...timeBlock,
                    background: color,
                    opacity: active ? 1 : 0.5,
                    outline: active ? "2px solid #000" : "none",
                  }}
                />
              );
            })}
          </div>

          <div style={{ marginTop: 8, fontSize: 14 }}>
            <span style={{ color: "#2ecc71" }}>🟢 Real</span> &nbsp;|&nbsp;
            <span style={{ color: "#f1c40f" }}>🟡 Suspicious</span> &nbsp;|&nbsp;
            <span style={{ color: "#e74c3c" }}>🔴 Manipulated</span> &nbsp;• Click to jump
          </div>

          {/* ===== SEGMENT LIST ===== */}
          {(segments.length > 0 || aiSegments.length > 0) && (
            <div style={{ marginTop: 8, fontSize: 14 }}>
              <b>Manipulated segments:</b>
              <ul style={{ marginTop: 4, marginLeft: 20 }}>
                {(segments.length > 0 ? segments : aiSegments).map((seg, i) => (
                  <li key={i}>
                    {formatTime(seg.start)} – {formatTime(seg.end)}
                    {seg.severity && ` (${seg.severity})`}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* ===== VERDICT SUMMARY ===== */}
      {verdict && (
        <div style={card}>
          <p>
            <b>Verdict:</b> <VerdictBadge verdict={verdict.verdict} />
          </p>
          <p>
            <b>Confidence:</b> {Math.round((1 - verdict.confidence) * 100)}% Real
          </p>
          <p>
            <b>Frames analyzed:</b> {verdict.frames_analyzed}
          </p>
        </div>
      )}

      {/* ===== FRAME TIMELINE ===== */}
      {frames.length > 0 && (
        <div style={card}>
          <h4>🧵 Suspicious Frames</h4>
          <div style={frameTimeline}>
            {frames.map((frame, idx) => {
              const prob = frame.ml_fake_probability || 0;
              const color =
                prob > 0.4
                  ? "#e74c3c"
                  : prob > 0.15
                  ? "#f1c40f"
                  : "#2ecc71";

              return (
                <img
                  key={idx}
                  src={frame.frame_path}
                  onClick={() => setSelectedFrame(frame)}
                  alt={`Frame ${idx}`}
                  style={{
                    ...thumb,
                    borderColor: color,
                  }}
                  onError={(e) => {
                    console.error(`Failed to load frame: ${frame.frame_path}`);
                    e.target.style.display = 'none';
                  }}
                />
              );
            })}
          </div>
        </div>
      )}

      {/* ===== FRAME DETAIL ===== */}
      {selectedFrame && (
        <div style={card}>
          <h4>🖼 Frame Detail</h4>
          <img
            src={selectedFrame.frame_path}
            alt="Selected frame"
            style={frameDetailStyle}
            onError={(e) => {
              console.error(`Failed to load selected frame: ${selectedFrame.frame_path}`);
              e.target.alt = "Failed to load frame image";
            }}
          />
          <p>
            <b>ML Fake Probability:</b>{" "}
            {(selectedFrame.ml_fake_probability * 100).toFixed(2)}%
          </p>
          <p>
            <b>Explanation:</b> {selectedFrame.explanation}
          </p>
        </div>
      )}

      {/* ===== SIGNAL BREAKDOWN ===== */}
      <div style={card}>
        <h4>📊 Signal Breakdown</h4>
        <SignalRow
          label="Temporal Consistency"
          value={signals.temporal?.verdict}
          ok={signals.temporal?.verdict === "stable"}
        />
        <SignalRow
          label="Motion Pattern"
          value={signals.motion?.verdict}
          ok={signals.motion?.verdict === "natural_motion"}
        />
        <SignalRow
          label="GAN Artifacts"
          value={signals.gan?.verdict}
          ok={false}
          note="Weak signal"
        />
      </div>
    </div>
  );
}

function SignalRow({ label, value, ok, note }) {
  return (
    <p>
      <b>{label}:</b>{" "}
      <span style={{ color: ok ? "green" : "orange" }}>
        {value || "N/A"}
      </span>
      {note && <span style={{ color: "#777" }}> ({note})</span>}
    </p>
  );
}

/* ===== STYLES ===== */

const card = {
  padding: 15,
  border: "1px solid #ddd",
  borderRadius: 6,
  marginBottom: 20,
};

const timelineBar = {
  display: "flex",
  gap: 2,
  overflowX: "auto",
};

const timeBlock = {
  width: 14,
  height: 20,
  cursor: "pointer",
  borderRadius: 2,
};

const frameTimeline = {
  display: "flex",
  gap: 10,
  overflowX: "auto",
  paddingBottom: 10,
};

const thumb = {
  width: 120,
  height: 80,
  objectFit: "cover",
  border: "3px solid transparent",
  borderRadius: 6,
  cursor: "pointer",
};

const videoStyle = {
  width: "70%",
  maxWidth: 400,
  borderRadius: 8,
  display: "block",
  margin: "0 auto",
  backgroundColor: "#f5f5f5",
  minHeight: 200,
};

const frameDetailStyle = {
  width: "50%",
  maxWidth: 300,
  borderRadius: 6,
  display: "block",
  margin: "10px auto",
  border: "1px solid #e5e7eb",
};

const errorContainer = {
  padding: 20,
  border: "2px dashed #e74c3c",
  borderRadius: 8,
  textAlign: "center",
  backgroundColor: "#fff5f5",
  marginBottom: 20,
};

export default VideoResult;