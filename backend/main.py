from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import tempfile
from typing import Optional
import mimetypes
from detectors import AIDetector

# Initialize FastAPI app
app = FastAPI(
    title="Digital Truth Scan API",
    description="AI-powered detection service for images, videos, and text",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI detector
detector = AIDetector()

def get_content_type(filename: str) -> str:
    """Determine content type based on file extension."""
    if not filename:
        return "unknown"
    
    # Get MIME type
    mime_type, _ = mimetypes.guess_type(filename)
    
    if mime_type:
        if mime_type.startswith('image/'):
            return "image"
        elif mime_type.startswith('video/'):
            return "video"
    
    # Fallback to file extension
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    
    image_extensions = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'tiff'}
    video_extensions = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv', 'm4v'}
    
    if ext in image_extensions:
        return "image"
    elif ext in video_extensions:
        return "video"
    
    return "unknown"

@app.post("/detect")
async def detect_content(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None)
):
    """
    Detect if uploaded content (image/video) or text is AI-generated.
    
    Either provide a file OR text content, not both.
    """
    try:
        # Validate input
        if file and text:
            raise HTTPException(
                status_code=400, 
                detail="Please provide either a file OR text, not both"
            )
        
        if not file and not text:
            raise HTTPException(
                status_code=400, 
                detail="Please provide either a file OR text content"
            )
        
        # Handle file upload
        if file:
            # Validate file size (max 100MB)
            if file.size and file.size > 100 * 1024 * 1024:
                raise HTTPException(
                    status_code=400, 
                    detail="File size too large. Maximum size is 100MB"
                )
            
            # Determine content type
            content_type = get_content_type(file.filename)
            if content_type not in ["image", "video"]:
                raise HTTPException(
                    status_code=400, 
                    detail="Unsupported file type. Please upload an image or video file"
                )
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as temp_file:
                content = await file.read()
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            try:
                # Perform detection
                result = detector.detect(
                    content_type=content_type,
                    content_path=temp_file_path
                )
                return JSONResponse(content=result)
            
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
        
        # Handle text input
        elif text:
            if not text.strip():
                raise HTTPException(
                    status_code=400, 
                    detail="Text content cannot be empty"
                )
            
            # Perform text detection
            result = detector.detect(
                content_type="text",
                text=text.strip()
            )
            return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error during detection"
        )

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Digital Truth Scan API",
        "version": "1.0.0",
        "endpoints": {
            "POST /detect": "Detect AI-generated content in images, videos, or text"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Digital Truth Scan API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
