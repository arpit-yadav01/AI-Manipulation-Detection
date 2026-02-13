import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import VideoUploader from '../components/VideoUploader';
import VideoResult from '../components/VideoResult';
import './DetectionPage.css';

function VideoDetectionPage() {
  const navigate = useNavigate();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <div className="detection-page">
      {/* Header */}
      <div className="detection-header">
        <button className="back-button" onClick={() => navigate('/')}>
          ← Back to Home
        </button>
        <h1 className="detection-title">
          <span className="icon">🎥</span>
          Video Deepfake Detection
        </h1>
        <p className="detection-subtitle">
          Upload a video to detect deepfakes, face-swaps, and temporal manipulations
        </p>
      </div>

      {/* Main Content */}
      <div className="detection-container">
        <div className="upload-section">
          <div className="upload-card">
            <div className="upload-icon">📹</div>
            <h2>Upload Video</h2>
            <p>Supported formats: MP4, WEBM, AVI (max 100MB)</p>
            
            <VideoUploader 
              onStart={() => setLoading(true)}
              onResult={(res) => {
                setResult(res);
                setLoading(false);
              }}
            />
            
            {loading && (
              <div className="loading-state">
                <div className="spinner"></div>
                <p>Analyzing video frames with deepfake detection...</p>
                <div className="loading-steps">
                  <div className="step">✓ Extracting frames</div>
                  <div className="step">✓ Facial landmark detection</div>
                  <div className="step active">⏳ Temporal consistency check</div>
                  <div className="step">○ Identity tracking</div>
                  <div className="step">○ GAN artifact detection</div>
                </div>
              </div>
            )}
          </div>

          {/* Info Cards */}
          <div className="info-cards">
            <div className="info-card">
              <div className="info-icon">🎭</div>
              <h3>Identity Tracking</h3>
              <p>Detects face-swap and identity inconsistencies</p>
            </div>
            <div className="info-card">
              <div className="info-icon">⏱️</div>
              <h3>Temporal Analysis</h3>
              <p>Frame-by-frame motion and consistency validation</p>
            </div>
            <div className="info-card">
              <div className="info-icon">🔬</div>
              <h3>GAN Detection</h3>
              <p>Identifies generative model artifacts</p>
            </div>
          </div>
        </div>

        {/* Results Section */}
        {result && (
          <div className="results-section">
            <VideoResult result={result} />
          </div>
        )}
      </div>
    </div>
  );
}

export default VideoDetectionPage;