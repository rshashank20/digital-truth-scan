import os
import tempfile
from typing import Tuple, Union, Dict, List
from datetime import datetime
import ffmpeg
from PIL import Image
import cv2
import torch
import torch.nn.functional as F
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
        
        # Get model labels for debugging
        self.image_labels = self.image_model.config.id2label
        self.text_labels = self.text_model.config.id2label
        
        # Debug mode
        self.debug = os.getenv('DETECTOR_DEBUG', 'false').lower() == 'true'
        
        if self.debug:
            print(f"Image model labels: {self.image_labels}")
            print(f"Text model labels: {self.text_labels}")
    
    def detect_image(self, image_path: str) -> Tuple[str, float, float, float]:
        """Detect if an image is AI-generated using the orion-ai/ai-image-detector model."""
        try:
            # Load and preprocess image using PIL
            image = Image.open(image_path).convert('RGB')
            
            # Use the model's feature extractor for proper preprocessing
            # This ensures correct resizing, normalization, and tensor conversion
            inputs = self.image_processor(image, return_tensors="pt").to(self.device)
            
            # Get prediction
            with torch.no_grad():
                outputs = self.image_model(**inputs)
                logits = outputs.logits
                
                # Apply softmax to get probabilities
                probs = F.softmax(logits, dim=-1)
                
                # Get probabilities for each class
                ai_prob = probs[0][1].item()  # Assuming index 1 is AI-generated
                real_prob = probs[0][0].item()  # Assuming index 0 is real
                
                # Debug logging
                if self.debug:
                    print(f"Image detection - Raw logits: {logits}")
                    print(f"Image detection - Probabilities: {probs}")
                    print(f"Image detection - AI prob: {ai_prob:.4f}, Real prob: {real_prob:.4f}")
                    print(f"Image detection - Labels: {self.image_labels}")
                    print(f"Image detection - Input shape: {inputs['pixel_values'].shape}")
                
                # Conservative verdict policy to reduce false positives on real content
                # We bias towards "inconclusive" in uncertain cases to avoid misclassifying real content as AI
                if ai_prob >= 0.85:
                    result = "likely_ai"
                elif ai_prob <= 0.25:
                    result = "real"
                else:
                    result = "inconclusive"
                
                # Return AI probability as confidence for transparency
                confidence = ai_prob
                
                return result, confidence, ai_prob, real_prob
                
        except Exception as e:
            print(f"Error detecting image: {e}")
            return "inconclusive", 0.0, 0.0, 0.0
    
    def detect_image_from_array(self, image_array: np.ndarray) -> Tuple[str, float]:
        """Detect if an image array is AI-generated (for video frame processing)."""
        try:
            # Convert numpy array to PIL Image
            image = Image.fromarray((image_array * 255).astype(np.uint8))
            inputs = self.image_processor(image, return_tensors="pt").to(self.device)
            
            # Get prediction
            with torch.no_grad():
                outputs = self.image_model(**inputs)
                logits = outputs.logits
                
                # Apply softmax to get probabilities
                probs = F.softmax(logits, dim=-1)
                
                # Get probabilities for each class
                ai_prob = probs[0][1].item()  # Assuming index 1 is AI-generated
                real_prob = probs[0][0].item()  # Assuming index 0 is real
                
                # Debug logging
                if self.debug:
                    print(f"Array image detection - Raw logits: {logits}")
                    print(f"Array image detection - Probabilities: {probs}")
                    print(f"Array image detection - AI prob: {ai_prob:.4f}, Real prob: {real_prob:.4f}")
                
                # Conservative verdict policy to reduce false positives on real content
                # We bias towards "inconclusive" in uncertain cases to avoid misclassifying real content as AI
                if ai_prob >= 0.85:
                    result = "likely_ai"
                elif ai_prob <= 0.25:
                    result = "real"
                else:
                    result = "inconclusive"
                
                # Return AI probability as confidence for transparency
                confidence = ai_prob
                
                return result, confidence
                
        except Exception as e:
            print(f"Error detecting image from array: {e}")
            return "inconclusive", 0.0
    
    def detect_video(self, video_path: str) -> Tuple[str, float, Dict]:
        """Detect if a video contains AI-generated content by analyzing frames."""
        try:
            # Extract frames using ffmpeg - sample 1 fps up to 64 frames
            frames_dir = tempfile.mkdtemp()
            
            # Get video info
            probe = ffmpeg.probe(video_path)
            duration = float(probe['streams'][0]['duration'])
            
            # Sample 1 fps, but limit to 64 frames maximum
            frame_interval = max(1.0, duration / 64)
            frame_times = np.arange(0, duration, frame_interval)
            
            frame_stats = []
            ai_probs = []
            quality_scores = []
            
            for i, time in enumerate(frame_times):
                frame_path = os.path.join(frames_dir, f"frame_{i:04d}.jpg")
                
                # Extract frame at specific time with high quality
                try:
                    (
                        ffmpeg
                        .input(video_path, ss=time)
                        .output(frame_path, vframes=1, q_v=1, pix_fmt='rgb24')
                        .overwrite_output()
                        .run(capture_stderr=True)
                    )
                    
                    # Load frame directly as RGB (ffmpeg already outputs RGB)
                    frame = cv2.imread(frame_path, cv2.IMREAD_COLOR)
                    if frame is None:
                        continue
                    
                    # Since ffmpeg outputs RGB24, we can use it directly
                    # But cv2.imread converts it back to BGR, so we need to convert back to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Calculate quality score using Laplacian variance
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
                    quality_scores.append(laplacian_var)
                    
                    # Skip low-quality frames (blurry)
                    if laplacian_var < 80:
                        os.remove(frame_path)
                        continue
                    
                    # Detect AI in frame using the RGB image
                    # The detect_image_from_array method will handle proper preprocessing
                    result, confidence, ai_prob, real_prob = self.detect_image_from_array(frame_rgb)
                    
                    # Store frame statistics
                    frame_stats.append({
                        "frame_number": i,
                        "timestamp": time,
                        "result": result,
                        "confidence": confidence,
                        "quality_score": laplacian_var
                    })
                    
                    # Store AI probability directly
                    ai_probs.append(confidence)
                    
                    # Clean up frame file
                    os.remove(frame_path)
                    
                except Exception as e:
                    print(f"Error processing frame at {time}s: {e}")
                    continue
            
            # Clean up frames directory
            os.rmdir(frames_dir)
            
            if not ai_probs:
                return "inconclusive", 0.0, {"frame_stats": frame_stats, "n_frames": 0, "pct_high": 0, "pct_low": 0}
            
            # Calculate robust statistics
            ai_probs = np.array(ai_probs)
            n_frames = len(ai_probs)
            
            # Trimmed mean (top 50% frames)
            sorted_probs = np.sort(ai_probs)
            trim_size = n_frames // 2
            final_prob = np.mean(sorted_probs[-trim_size:])
            
            # Calculate percentage statistics
            pct_high = np.sum(ai_probs >= 0.7) / n_frames * 100
            pct_low = np.sum(ai_probs <= 0.3) / n_frames * 100
            
            # Enhanced verdict rules with robust statistics
            if final_prob >= 0.85 and pct_high >= 70:
                result = "likely_ai"
            elif final_prob <= 0.25 and pct_low >= 70:
                result = "real"
            else:
                result = "inconclusive"
            
            # Enhanced frame statistics for transparency
            enhanced_stats = {
                "frame_stats": frame_stats,
                "n_frames": n_frames,
                "pct_high": round(pct_high, 1),
                "pct_low": round(pct_low, 1),
                "final_prob": round(final_prob, 4),
                "quality_threshold": 80
            }
            
            return result, final_prob, enhanced_stats
            
        except Exception as e:
            print(f"Error detecting video: {e}")
            return "inconclusive", 0.0, {}
    
    def detect_text(self, text: str) -> Tuple[str, float, float, float]:
        """Detect if text is AI-generated using the roberta-base-openai-detector model."""
        try:
            # Tokenize and run through model
            inputs = self.text_tokenizer(
                text, 
                return_tensors="pt", 
                truncation=True, 
                padding=True
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.text_model(**inputs)
                
            logits = outputs.logits
            probs = F.softmax(logits, dim=-1)[0].tolist()
            
            # HuggingFace order: [real_prob, fake_prob]
            real_prob = probs[0]
            ai_prob = probs[1]
            
            # Debug logging
            if self.debug:
                print(f"Text detection - Raw logits: {logits}")
                print(f"Text detection - Probabilities: {probs}")
                print(f"Text detection - AI prob: {ai_prob:.4f}, Real prob: {real_prob:.4f}")
                print(f"Text detection - Labels: {self.text_labels}")
            
            # Decide verdict
            if ai_prob >= 0.85:
                result = "likely_ai"
            elif ai_prob <= 0.25:
                result = "real"
            else:
                result = "inconclusive"
            
            # Return AI probability as confidence for transparency
            confidence = ai_prob
            
            return result, confidence, ai_prob, real_prob
                
        except Exception as e:
            print(f"Error detecting text: {e}")
            return "inconclusive", 0.0, 0.0, 0.0
    
    def detect(self, content_type: str, content_path: str = None, text: str = None) -> dict:
        """Main detection method that routes to appropriate detector."""
        checked_at = datetime.utcnow().isoformat() + "Z"
        
        try:
            if content_type == "image":
                if not content_path:
                    raise ValueError("Image path required for image detection")
                result, confidence, ai_prob, real_prob = self.detect_image(content_path)
                frame_stats = None
                
            elif content_type == "video":
                if not content_path:
                    raise ValueError("Video path required for video detection")
                result, confidence, frame_stats = self.detect_video(content_path)
                # For video, we'll use the final_prob as ai_prob and calculate real_prob
                ai_prob = confidence
                real_prob = 1.0 - confidence
                
            elif content_type == "text":
                if not text:
                    raise ValueError("Text content required for text detection")
                result, confidence, ai_prob, real_prob = self.detect_text(text)
                frame_stats = None
                
            else:
                raise ValueError(f"Unsupported content type: {content_type}")
            
            response = {
                "type": content_type,
                "result": result,
                "confidence": round(confidence, 4),
                "ai_prob": round(ai_prob, 4),
                "real_prob": round(real_prob, 4),
                "checked_at": checked_at
            }
            
            # Add frame statistics for video
            if frame_stats:
                response["frame_stats"] = frame_stats
            
            return response
            
        except Exception as e:
            print(f"Detection error: {e}")
            return {
                "type": content_type,
                "result": "inconclusive",
                "confidence": 0.0,
                "checked_at": checked_at
            }
