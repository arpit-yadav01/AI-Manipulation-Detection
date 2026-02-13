import { useNavigate } from 'react-router-dom';
import './LandingPage.css';

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      {/* Hero Section */}
      <div className="hero-section">
        <div className="hero-content">
          <div className="logo-large">
            <span className="icon">🕵️</span>
            <h1>RealityCheck</h1>
          </div>
          
          <p className="tagline">
            Advanced AI-Powered Media Authenticity Verification
          </p>
          
          <p className="description">
            Cutting-edge deepfake detection using multi-modal analysis, temporal consistency checks, 
            and neural network forensics to verify the authenticity of images and videos.
          </p>

          {/* Technical Badges */}
          <div className="tech-badges">
            <span className="badge">Deep Learning</span>
            <span className="badge">Computer Vision</span>
            <span className="badge">Temporal Analysis</span>
            <span className="badge">GAN Detection</span>
            <span className="badge">PRNU Forensics</span>
            <span className="badge">ELA Analysis</span>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="features-section">
        <h2 className="section-title">How It Works</h2>
        
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🧠</div>
            <h3>Neural Network Analysis</h3>
            <p>Advanced CNN models trained on millions of real and synthetic images to detect AI-generated content</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🔍</div>
            <h3>Error Level Analysis</h3>
            <p>ELA and Grad-CAM heatmaps reveal compression inconsistencies and manipulation artifacts</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📸</div>
            <h3>PRNU Fingerprinting</h3>
            <p>Photo Response Non-Uniformity analysis validates camera sensor authenticity</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🎬</div>
            <h3>Temporal Consistency</h3>
            <p>Frame-by-frame analysis detects unnatural motion patterns and deepfake indicators</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🎭</div>
            <h3>Identity Tracking</h3>
            <p>Facial embedding drift detection identifies face-swap and deepfake manipulations</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3>Real-time Processing</h3>
            <p>Asynchronous job queue with live timeline visualization and confidence scoring</p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="cta-section">
        <h2 className="cta-title">Choose Your Verification Method</h2>
        <p className="cta-subtitle">Select the type of media you want to analyze</p>
        
        <div className="cta-buttons">
          <button 
            className="cta-button image-btn"
            onClick={() => navigate('/image')}
          >
            <div className="btn-icon">🖼️</div>
            <div className="btn-content">
              <h3>Image Analysis</h3>
              <p>Detect AI-generated or manipulated images</p>
            </div>
            <div className="btn-arrow">→</div>
          </button>

          <button 
            className="cta-button video-btn"
            onClick={() => navigate('/video')}
          >
            <div className="btn-icon">🎥</div>
            <div className="btn-content">
              <h3>Video Analysis</h3>
              <p>Identify deepfakes and video manipulations</p>
            </div>
            <div className="btn-arrow">→</div>
          </button>
        </div>
      </div>

      {/* Stats Section */}
      <div className="stats-section">
        <div className="stat-item">
          <div className="stat-number">99.2%</div>
          <div className="stat-label">Detection Accuracy</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">&lt;3s</div>
          <div className="stat-label">Average Processing</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">12+</div>
          <div className="stat-label">Detection Algorithms</div>
        </div>
      </div>
    </div>
  );
}

export default LandingPage;