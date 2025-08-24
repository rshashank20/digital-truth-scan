import os
import tempfile
from typing import Tuple, Union
from datetime import datetime
import ffmpeg
from PIL import Image
import torch
from transformers import (
    AutoImageProcessor, 
    AutoModelForImageClassification,
    AutoTokenizer,
    AutoModelForSequenceClassification,
    pipeline
)
import numpy as np

class AIDetector:
    def __init__(self):
        # Initialize image detection model
        self.image_processor = AutoImageProcessor.from_pretrained("orion-ai/ai-image-detector")
        self.image_model = AutoModelForImageClassification.from_pretrained("orion-ai/ai-image-detector")
        
        # Initialize text detection model
        self.text_tokenizer = AutoTokenizer.from_pretrained("roberta-base-openai-detector")
        self.text_model = AutoModelForSequenceClassification.from_pretrained("roberta-base-openai-detector")
        
        # Move models to GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.image_model.to(self.device)
        self.text_model.to(self.device)
        
        # Set models to evaluation mode
        self.image_model.eval()
        self.text_model.eval()
    
    def detect_image(self, image_path: str) -> Tuple[str, float]:
        """Detect if an image is AI-generated using the orion-ai/ai-image-detector model."""
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            inputs = self.image_processor(image, return_tensors="pt").to(self.device)
            
            # Get prediction
            with torch.no_grad():
                outputs = self.image_model(**inputs)
                probabilities = torch.softmax(outputs.logits, dim=1)
            
            # Get confidence and prediction
            confidence, predicted_class = torch.max(probabilities, 1)
            confidence = confidence.item()
            predicted_class = predicted_class.item()
            
            # Map prediction to result
            # Model outputs: 0 = real, 1 = AI-generated
            if predicted_class == 0:
                result = "real"
            else:
                result = "likely_ai"
            
            return result, confidence
            
        except Exception as e:
            print(f"Error detecting image: {e}")
            return "inconclusive", 0.0
    
    def detect_video(self, video_path: str) -> Tuple[str, float]:
        """Detect if a video contains AI-generated content by analyzing frames."""
        try:
            # Extract frames using ffmpeg
            frames_dir = tempfile.mkdtemp()
            
            # Get video info
            probe = ffmpeg.probe(video_path)
            duration = float(probe['streams'][0]['duration'])
            
            # Extract frames every 2 seconds
            frame_interval = 2.0
            frame_times = np.arange(0, duration, frame_interval)
            
            results = []
            confidences = []
            
            for i, time in enumerate(frame_times):
                frame_path = os.path.join(frames_dir, f"frame_{i:04d}.jpg")
                
                # Extract frame at specific time
                try:
                    (
                        ffmpeg
                        .input(video_path, ss=time)
                        .output(frame_path, vframes=1, q:v=2)
                        .overwrite_output()
                        .run(capture_stdout=True, capture_stderr=True)
                    )
                    
                    # Detect AI in frame
                    result, confidence = self.detect_image(frame_path)
                    results.append(result)
                    confidences.append(confidence)
                    
                    # Clean up frame file
                    os.remove(frame_path)
                    
                except Exception as e:
                    print(f"Error extracting frame at {time}s: {e}")
                    continue
            
            # Clean up frames directory
            os.rmdir(frames_dir)
            
            if not results:
                return "inconclusive", 0.0
            
            # Calculate average confidence
            avg_confidence = np.mean(confidences)
            
            # Determine overall result based on majority of frames
            ai_count = sum(1 for r in results if r == "likely_ai")
            real_count = sum(1 for r in results if r == "real")
            
            if ai_count > real_count:
                result = "likely_ai"
            elif real_count > ai_count:
                result = "real"
            else:
                result = "inconclusive"
            
            return result, avg_confidence
            
        except Exception as e:
            print(f"Error detecting video: {e}")
            return "inconclusive", 0.0
    
    def detect_text(self, text: str) -> Tuple[str, float]:
        """Detect if text is AI-generated using the roberta-base-openai-detector model."""
        try:
            # Tokenize and get prediction
            inputs = self.text_tokenizer(
                text, 
                return_tensors="pt", 
                truncation=True, 
                max_length=512
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.text_model(**inputs)
                probabilities = torch.softmax(outputs.logits, dim=1)
            
            # Get confidence and prediction
            confidence, predicted_class = torch.max(probabilities, 1)
            confidence = confidence.item()
            predicted_class = predicted_class.item()
            
            # Map prediction to result
            # Model outputs: 0 = human, 1 = AI-generated
            if predicted_class == 0:
                result = "real"
            else:
                result = "likely_ai"
            
            return result, confidence
            
        except Exception as e:
            print(f"Error detecting text: {e}")
            return "inconclusive", 0.0
    
    def detect(self, content_type: str, content_path: str = None, text: str = None) -> dict:
        """Main detection method that routes to appropriate detector."""
        checked_at = datetime.utcnow().isoformat() + "Z"
        
        try:
            if content_type == "image":
                if not content_path:
                    raise ValueError("Image path required for image detection")
                result, confidence = self.detect_image(content_path)
                
            elif content_type == "video":
                if not content_path:
                    raise ValueError("Video path required for video detection")
                result, confidence = self.detect_video(content_path)
                
            elif content_type == "text":
                if not text:
                    raise ValueError("Text content required for text detection")
                result, confidence = self.detect_text(text)
                
            else:
                raise ValueError(f"Unsupported content type: {content_type}")
            
            return {
                "type": content_type,
                "result": result,
                "confidence": round(confidence, 3),
                "checked_at": checked_at
            }
            
        except Exception as e:
            print(f"Detection error: {e}")
            return {
                "type": content_type,
                "result": "inconclusive",
                "confidence": 0.0,
                "checked_at": checked_at
            }
