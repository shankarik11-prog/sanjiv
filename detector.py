"""
MoodLens - Core Emotion Detection Engine
Detects facial emotions using OpenCV + DeepFace and maps them
to personalized recommendations.
"""

import cv2
import numpy as np
from deepface import DeepFace
from typing import Optional
import logging

logger = logging.getLogger(__name__)


EMOTION_LABELS = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]

# Color palette for each emotion (BGR for OpenCV)
EMOTION_COLORS = {
    "angry":    (0,   0,   220),
    "disgust":  (0,   140, 0  ),
    "fear":     (128, 0,   128),
    "happy":    (0,   200, 255),
    "sad":      (180, 80,  0  ),
    "surprise": (0,   165, 255),
    "neutral":  (160, 160, 160),
}


class EmotionDetector:
    """
    Real-time face emotion detector using OpenCV face detection
    and DeepFace for emotion classification.
    """

    def __init__(self, backend: str = "opencv", model_name: str = "Emotion"):
        self.backend = backend
        self.model_name = model_name
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def detect_faces(self, frame: np.ndarray) -> list[tuple]:
        """Detect face bounding boxes in frame."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60)
        )
        return faces if len(faces) > 0 else []

    def analyze_emotion(self, frame: np.ndarray) -> Optional[dict]:
        """
        Run DeepFace emotion analysis on a frame.
        Returns dict with dominant emotion + all scores, or None if no face found.
        """
        try:
            results = DeepFace.analyze(
                frame,
                actions=["emotion"],
                enforce_detection=False,
                detector_backend=self.backend,
                silent=True,
            )
            if results:
                result = results[0]
                return {
                    "dominant": result["dominant_emotion"],
                    "scores": result["emotion"],
                    "region": result.get("region", {}),
                }
        except Exception as e:
            logger.debug(f"DeepFace analysis error: {e}")
        return None

    def annotate_frame(self, frame: np.ndarray, analysis: dict) -> np.ndarray:
        """Draw emotion label + confidence bar on frame."""
        frame = frame.copy()
        dominant = analysis["dominant"]
        scores = analysis["scores"]
        region = analysis.get("region", {})
        color = EMOTION_COLORS.get(dominant, (255, 255, 255))

        # Draw face bounding box if region available
        if region:
            x, y, w, h = region.get("x", 0), region.get("y", 0), region.get("w", 0), region.get("h", 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        # Emotion label
        cv2.putText(
            frame, f"Mood: {dominant.upper()}",
            (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2
        )

        # Confidence bars
        bar_x, bar_y = 10, 60
        for i, (emotion, score) in enumerate(sorted(scores.items(), key=lambda x: -x[1])):
            bar_len = int(score * 1.5)
            ec = EMOTION_COLORS.get(emotion, (200, 200, 200))
            cv2.rectangle(frame, (bar_x, bar_y + i * 22), (bar_x + bar_len, bar_y + i * 22 + 16), ec, -1)
            cv2.putText(
                frame, f"{emotion[:3]} {score:.0f}%",
                (bar_x + bar_len + 5, bar_y + i * 22 + 13),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (220, 220, 220), 1
            )

        return frame
