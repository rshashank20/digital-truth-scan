# 🚀 Digital Truth Scan

> **AI-Powered Content Authenticity Detection Platform**

[![React](https://img.shields.io/badge/React-18.0.0-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue.svg)](https://www.typescriptlang.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8.1-orange.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive web application that detects AI-generated content in images, videos, and text using state-of-the-art machine learning models. Built with React + TypeScript frontend and FastAPI backend, featuring advanced preprocessing and robust detection algorithms.

## ✨ Features

### 🔍 **Multi-Modal Detection**
- **🖼️ Image Analysis**: Detect AI-generated images using `orion-ai/ai-image-detector` with optimal preprocessing
- **🎥 Video Processing**: Advanced frame extraction with quality filtering and robust statistics
- **📝 Text Analysis**: Identify AI-generated text using `roberta-base-openai-detector` with enhanced tokenization

### 🎨 **Modern Frontend**
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Results**: Instant detection results with dual probability scores
- **File Upload**: Drag & drop support for images and videos
- **History Tracking**: Save and review previous detection results
- **Beautiful UI**: Built with Tailwind CSS and shadcn/ui components

### ⚡ **High-Performance Backend**
- **FastAPI Framework**: Modern, fast Python web framework
- **GPU Acceleration**: CUDA support for faster inference
- **Advanced Preprocessing**: HuggingFace AutoImageProcessor for optimal model performance
- **Quality Filtering**: Laplacian variance-based blur detection for video frames
- **CORS Enabled**: Ready for frontend integration
- **RESTful API**: Clean, documented endpoints with comprehensive responses

### 🔬 **Enhanced Detection Capabilities**
- **Conservative Verdict Policy**: Reduces false positives on real content
- **Dual Probability Output**: Both AI and real probabilities for transparency
- **Robust Video Analysis**: Trimmed mean statistics and quality filtering
- **Debug Mode**: Environment variable controlled logging for development

## 🏗️ Architecture

```
digital-truth-scan/
├── 📁 frontend/                 # React + TypeScript application
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/             # Application pages
│   │   ├── hooks/             # Custom React hooks
│   │   └── services/          # API integration
│   └── package.json
├── 📁 backend/                  # FastAPI Python service
│   ├── main.py                # FastAPI application with CORS
│   ├── detectors.py           # Advanced AI detection logic
│   ├── requirements.txt       # Python dependencies
│   └── run.py                 # Server startup script
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ and **npm**/**yarn**
- **Python** 3.8+
- **FFmpeg** (for video processing)
- **OpenCV** (automatically installed via pip)

### 1. Clone the Repository
```bash
git clone https://github.com/rshashank20/digital-truth-scan.git
cd digital-truth-scan
```

### 2. Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```
Frontend will be available at `http://localhost:5173`

### 3. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
python run.py
```
Backend will be available at `http://localhost:8000`

### 4. Install FFmpeg
- **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html) or use `choco install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

## 📡 API Endpoints

### POST `/detect`
Detect AI-generated content in uploaded files or text with enhanced response format.

**Request:**
```bash
# Upload image/video
curl -X POST "http://localhost:8000/detect" \
     -F "file=@image.jpg"

# Analyze text
curl -X POST "http://localhost:8000/detect" \
     -d "text=This is some text to analyze"
```

**Enhanced Response:**
```json
{
  "type": "image|video|text",
  "result": "real|likely_ai|inconclusive",
  "confidence": 0.0-1.0,
  "ai_prob": 0.0-1.0,
  "real_prob": 0.0-1.0,
  "checked_at": "2024-01-01T12:00:00Z",
  "frame_stats": {
    "n_frames": 32,
    "pct_high": 75.0,
    "pct_low": 15.0,
    "final_prob": 0.8234,
    "quality_threshold": 80
  }
}
```

### GET `/`
API information and available endpoints.

### GET `/health`
Health check endpoint.

## 🔬 Detection Algorithms

### 🖼️ **Image Detection**
- **Model**: `orion-ai/ai-image-detector`
- **Preprocessing**: HuggingFace AutoImageProcessor for optimal performance
- **Verdict Policy**: Conservative thresholds (AI ≥ 85%, Real ≤ 25%, else Inconclusive)
- **Output**: Dual probabilities for transparency

### 🎥 **Video Detection**
- **Frame Sampling**: 1 FPS up to 64 frames maximum
- **Quality Filtering**: Laplacian variance threshold (80) to exclude blurry frames
- **Robust Statistics**: Trimmed mean of top 50% AI probability frames
- **Enhanced Verdict**: Combines final probability with percentage statistics
- **Frame Analysis**: Comprehensive statistics for transparency

### 📝 **Text Detection**
- **Model**: `roberta-base-openai-detector`
- **Tokenization**: Optimized with padding and truncation
- **Probability Mapping**: Correct HuggingFace label order `[real_prob, fake_prob]`
- **Verdict Policy**: Same conservative thresholds as image detection

## 🛠️ Development

### Frontend Development
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
```

### Backend Development
```bash
cd backend
python run.py        # Start with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Debug Mode
Enable detailed logging for development:
```bash
# Set environment variable
set DETECTOR_DEBUG=true  # Windows
# export DETECTOR_DEBUG=true  # macOS/Linux

# Run backend
python run.py
```

### API Documentation
Once the backend is running, visit:
- **Interactive Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔧 Configuration

### CORS Settings
The backend is configured with permissive CORS for development. In production, restrict origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Environment Variables
Create `.env` files for configuration:

**Frontend (.env):**
```env
VITE_API_URL=http://localhost:8000
```

**Backend (.env):**
```env
DETECTOR_DEBUG=false
MODEL_CACHE_DIR=./models
MAX_FILE_SIZE=104857600  # 100MB
```

## 📊 Performance & Quality

### **Detection Accuracy**
- **Conservative Policy**: Biased towards "inconclusive" to reduce false positives
- **Quality Filtering**: Automatic exclusion of low-quality video frames
- **Robust Statistics**: Trimmed mean aggregation for reliable video analysis

### **Performance Notes**
- **First Request**: Models load on first use (10-30 seconds)
- **GPU Acceleration**: Automatic CUDA detection for faster inference
- **Video Processing**: Optimized frame extraction with quality filtering
- **Memory Management**: Automatic cleanup of temporary files and frames

### **Quality Thresholds**
- **Image/Text**: AI ≥ 85% → "likely_ai", Real ≤ 25% → "real"
- **Video**: Enhanced rules with frame statistics and percentage thresholds
- **Frame Quality**: Laplacian variance ≥ 80 for clear, non-blurry frames

## 🐛 Troubleshooting

### Common Issues

1. **FFmpeg not found**
   - Ensure FFmpeg is installed and in your PATH
   - Verify with `ffmpeg -version`

2. **CUDA out of memory**
   - Models will automatically fall back to CPU
   - Reduce batch size if needed

3. **Model download issues**
   - Check internet connection
   - Verify Hugging Face access
   - Clear model cache: `rm -rf ~/.cache/huggingface/`

4. **Port conflicts**
   - Frontend: Change port in `vite.config.ts`
   - Backend: Use `python run.py 8001` for different port

5. **OpenCV installation issues**
   - Ensure Python 3.8+ compatibility
   - Try: `pip install --upgrade opencv-python`

### Debug Mode
```bash
# Frontend
npm run dev -- --debug

# Backend
set DETECTOR_DEBUG=true  # Windows
python run.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face** for the AI detection models
- **FastAPI** for the excellent Python web framework
- **React** and **TypeScript** for the frontend framework
- **Tailwind CSS** and **shadcn/ui** for the beautiful UI components
- **OpenCV** for advanced image processing capabilities
- **FFmpeg** for robust video frame extraction

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/rshashank20/digital-truth-scan/issues)
- **Discussions**: [GitHub Discussions](https://github.com/rshashank20/digital-truth-scan/discussions)
- **Email**: [Your Email]

---

<div align="center">
  <p>Made with ❤️ by <a href="https://github.com/rshashank20">rshashank20</a></p>
  <p>⭐ Star this repo if you found it helpful!</p>
</div>
