import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ImageUploader from '../components/ImageUploader';
import ImageResult from '../components/ImageResult';
import { useJobPolling } from '../hooks/useJobPolling';
import './DetectionPage.css';

function ImageDetectionPage() {
  const navigate = useNavigate();
  const [jobId, setJobId] = useState(null);
  const { result, loading } = useJobPolling(jobId);

  return (
    <div className="detection-page">
      {/* Header */}
      <div className="detection-header">
        <button className="back-button" onClick={() => navigate('/')}>
          ← Back to Home
        </button>
        <h1 className="detection-title">
          <span className="icon">🖼️</span>
          Image Authenticity Analysis
        </h1>
        <p className="detection-subtitle">
          Upload an image to detect AI manipulation, deepfakes, and digital forgeries
        </p>
      </div>

      {/* Main Content */}
      <div className="detection-container">
        <div className="upload-section">
          <div className="upload-card">
            <div className="upload-icon">📤</div>
            <h2>Upload Image</h2>
            <p>Supported formats: JPG, PNG, WEBP</p>
            
            <ImageUploader onJobCreated={setJobId} />
            
            {loading && (
              <div className="loading-state">
                <div className="spinner"></div>
                <p>Analyzing image with AI detection algorithms...</p>
                <div className="loading-steps">
                  <div className="step">✓ Extracting features</div>
                  <div className="step">✓ Running ELA analysis</div>
                  <div className="step active">⏳ Generating heatmap</div>
                  <div className="step">○ Computing verdict</div>
                </div>
              </div>
            )}
          </div>

          {/* Info Cards */}
          <div className="info-cards">
            <div className="info-card">
              <div className="info-icon">🧠</div>
              <h3>ML Classification</h3>
              <p>Deep neural networks trained on millions of images</p>
            </div>
            <div className="info-card">
              <div className="info-icon">🔥</div>
              <h3>ELA Heatmap</h3>
              <p>Visualize compression artifacts and manipulation zones</p>
            </div>
            <div className="info-card">
              <div className="info-icon">📸</div>
              <h3>PRNU Analysis</h3>
              <p>Camera sensor fingerprint validation</p>
            </div>
          </div>
        </div>

        {/* Results Section */}
        {result && (
          <div className="results-section">
            <ImageResult result={result} />
          </div>
        )}
      </div>
    </div>
  );
}

export default ImageDetectionPage;