// import { useState } from "react";
// import { useJobPolling } from "../hooks/useJobPolling";

// function VideoUploader({ onStart, onResult }) {
//   const [file, setFile] = useState(null);
//   const { pollResult } = useJobPolling();

//   const uploadVideo = async () => {
//     if (!file) return alert("Select a video file");

//     onStart();

//     const formData = new FormData();
//     formData.append("file", file);

//     const res = await fetch("http://localhost:8000/api/video/analyze", {
//       method: "POST",
//       body: formData,
//     });

//     const data = await res.json();
//     pollResult(data.job_id, onResult);
//   };

//   return (
//     <div style={{ marginBottom: 30 }}>
//       <h3>🎥 Video Authenticity</h3>

//       <input
//         type="file"
//         accept="video/*"
//         onChange={(e) => setFile(e.target.files[0])}
//       />
//       <br /><br />

//       <button onClick={uploadVideo}>Analyze Video</button>
//     </div>
//   );
// }

// export default VideoUploader;



import { useState } from "react";

function VideoUploader({ onStart, onResult }) {
  const [file, setFile] = useState(null);

  const pollResult = async (jobId, callback) => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/result/${jobId}`);
        const data = await res.json();

        if (data.status === "done") {
          clearInterval(interval);
          callback(data);
        }

        if (data.status === "error") {
          clearInterval(interval);
          console.error("❌ Job failed:", data.error || "Unknown error");
          callback({ error: data.error });
        }
      } catch (err) {
        console.error("Polling error:", err);
      }
    }, 2000);
  };

  const uploadVideo = async () => {
    if (!file) return alert("Select a video file");

    onStart();

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/api/video/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      
      if (data.job_id) {
        pollResult(data.job_id, onResult);
      } else {
        console.error("No job_id received from server");
        alert("Failed to start video analysis");
      }
    } catch (error) {
      console.error("Upload error:", error);
      alert("Failed to upload video");
    }
  };

  return (
    <div style={{ marginBottom: 30 }}>
      <h3>🎥 Video Authenticity</h3>

      <input
        type="file"
        accept="video/*"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <br /><br />

      <button onClick={uploadVideo}>Analyze Video</button>
    </div>
  );
}

export default VideoUploader;