// import { useState } from "react";
// import { uploadImage, uploadVideo } from "./api/client";
// import { useJobPolling } from "./hooks/useJobPolling";

// import Header from "./components/Header";
// import Footer from "./components/Footer";
// import ImageResult from "./components/ImageResult";
// import VideoResult from "./components/VideoResult";

// function App() {
//   const [file, setFile] = useState(null);
//   const [jobId, setJobId] = useState(null);
//   const [mode, setMode] = useState(null); // "image" | "video"

//   const { result, loading } = useJobPolling(jobId);

//   async function handleUpload(selectedMode) {
//     if (!file) {
//       alert("Please select a file first");
//       return;
//     }

//     setMode(selectedMode);

//     const data =
//       selectedMode === "image"
//         ? await uploadImage(file)
//         : await uploadVideo(file);

//     setJobId(data.job_id);
//   }

//   return (
//     <>
//       <Header />

//       <main style={main}>
//         {/* ===== HERO / UPLOAD SECTION ===== */}
//         <section style={hero}>
//           <h1 style={title}>Analyze Images & Videos for AI Manipulation</h1>
//           <p style={subtitle}>
//             Upload content to detect AI-generated or manipulated media.
//           </p>

//           {/* Upload Cards */}
//           <div style={uploadGrid}>
//             {/* IMAGE CARD */}
//             <div style={card}>
//               <h3>🖼 Analyze Image</h3>
//               <p style={hint}>JPG, PNG</p>

//               <input
//                 type="file"
//                 accept="image/*"
//                 onChange={(e) => setFile(e.target.files[0])}
//               />

//               <button
//                 style={{ ...button, background: "#2563eb" }}
//                 onClick={() => handleUpload("image")}
//               >
//                 Analyze Image
//               </button>
//             </div>

//             {/* VIDEO CARD */}
//             <div style={card}>
//               <h3>🎬 Analyze Video</h3>
//               <p style={hint}>MP4</p>

//               <input
//                 type="file"
//                 accept="video/*"
//                 onChange={(e) => setFile(e.target.files[0])}
//               />

//               <button
//                 style={{ ...button, background: "#7c3aed" }}
//                 onClick={() => handleUpload("video")}
//               >
//                 Analyze Video
//               </button>
//             </div>
//           </div>
//         </section>

//         {/* ===== STATUS ===== */}
//         {loading && <p style={loadingText}>⏳ Analyzing…</p>}

//         {/* ===== RESULTS ===== */}
//         {result && mode === "image" && <ImageResult result={result} />}
//         {result && mode === "video" && <VideoResult result={result} />}
//       </main>

//       <Footer />
//     </>
//   );
// }

// /* ================= STYLES ================= */

// const main = {
//   maxWidth: 1100,
//   margin: "0 auto",
//   padding: "40px 20px",
// };

// const hero = {
//   textAlign: "center",
//   marginBottom: 60,
// };

// const title = {
//   fontSize: 32,
//   fontWeight: 600,
// };

// const subtitle = {
//   marginTop: 10,
//   fontSize: 16,
//   color: "#6b7280",
// };

// const uploadGrid = {
//   display: "flex",
//   gap: 20,
//   justifyContent: "center",
//   flexWrap: "wrap",
//   marginTop: 40,
// };

// const card = {
//   width: 280,
//   padding: 20,
//   borderRadius: 8,
//   border: "1px solid #e5e7eb",
//   background: "#ffffff",
//   textAlign: "center",
// };

// const hint = {
//   fontSize: 14,
//   color: "#6b7280",
//   marginBottom: 10,
// };

// const button = {
//   marginTop: 15,
//   padding: "10px 16px",
//   borderRadius: 6,
//   border: "none",
//   color: "white",
//   fontWeight: 500,
//   cursor: "pointer",
//   width: "100%",
// };

// const loadingText = {
//   marginTop: 30,
//   fontSize: 16,
// };

// export default App;


import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import ImageDetectionPage from './pages/ImageDetectionPage';
import VideoDetectionPage from './pages/VideoDetectionPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/image" element={<ImageDetectionPage />} />
          <Route path="/video" element={<VideoDetectionPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;