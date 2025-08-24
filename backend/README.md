# Digital Truth Scan Backend

A FastAPI backend service for detecting AI-generated content in images, videos, and text using state-of-the-art Hugging Face models.

## Features

- **Image Detection**: Uses `orion-ai/ai-image-detector` model to detect AI-generated images
- **Video Detection**: Extracts frames from videos and analyzes them using the same image detection model
- **Text Detection**: Uses `roberta-base-openai-detector` model to detect AI-generated text
- **RESTful API**: Clean FastAPI endpoints with automatic documentation
- **CORS Support**: Configured for frontend integration

## Requirements

- Python 3.8+
- FFmpeg (for video processing)
- CUDA-compatible GPU (optional, for faster inference)

## Installation

1. **Install FFmpeg** (required for video processing):
   - **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html) or use Chocolatey: `choco install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo yum install ffmpeg` (CentOS/RHEL)

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Server

```bash
# Development mode
python main.py

# Or using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The server will start on `http://localhost:8000`

### API Documentation

Once running, visit:
- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`

## API Endpoints

### POST /detect

Detect AI-generated content in uploaded files or text.

**Parameters:**
- `file` (optional): Uploaded image or video file
- `text` (optional): Text content to analyze

**Note**: Provide either `file` OR `text`, not both.

**Response Format:**
```json
{
  "type": "image|video|text",
  "result": "real|likely_ai|inconclusive",
  "confidence": 0.0-1.0,
  "checked_at": "2024-01-01T12:00:00Z"
}
```

**Example Usage:**

1. **Upload an image**:
   ```bash
   curl -X POST "http://localhost:8000/detect" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@image.jpg"
   ```

2. **Analyze text**:
   ```bash
   curl -X POST "http://localhost:8000/detect" \
        -H "accept: application/json" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "text=This is some text to analyze"
   ```

### GET /

Returns API information and available endpoints.

### GET /health

Health check endpoint.

## Models Used

- **Image/Video Detection**: `orion-ai/ai-image-detector`
  - Outputs: 0 = real, 1 = AI-generated
  - Specialized for detecting AI-generated images

- **Text Detection**: `roberta-base-openai-detector`
  - Outputs: 0 = human, 1 = AI-generated
  - Trained to detect AI-generated text

## Configuration

### CORS Settings

The backend is configured with permissive CORS settings for development. In production, restrict the `allow_origins` to your frontend domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### File Size Limits

Maximum file upload size is set to 100MB. Adjust this in the `/detect` endpoint if needed.

## Error Handling

The API returns appropriate HTTP status codes:
- `400`: Bad request (invalid input, unsupported file type, etc.)
- `500`: Internal server error

All errors include descriptive error messages in the response.

## Performance Notes

- **First Request**: Models are loaded on first use, which may take 10-30 seconds
- **GPU Acceleration**: If CUDA is available, models will automatically use GPU for faster inference
- **Video Processing**: Video analysis extracts frames every 2 seconds to balance accuracy and performance

## Troubleshooting

### Common Issues

1. **FFmpeg not found**: Ensure FFmpeg is installed and accessible in your PATH
2. **CUDA out of memory**: Reduce batch size or use CPU-only mode
3. **Model download issues**: Check internet connection and Hugging Face access

### Debug Mode

Enable debug logging by setting the log level:
```bash
uvicorn main:app --log-level debug
```

## Development

### Project Structure

```
backend/
├── main.py          # FastAPI application and endpoints
├── detectors.py     # AI detection logic and models
├── requirements.txt # Python dependencies
└── README.md       # This file
```

### Adding New Models

To add new detection models, extend the `AIDetector` class in `detectors.py` and add corresponding endpoints in `main.py`.

## License

This project is part of the Digital Truth Scan application.
