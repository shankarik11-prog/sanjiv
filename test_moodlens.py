"""
MoodLens - Unit Tests
Run: pytest tests/
"""

import pytest
import numpy as np
from moodlens.recommender import RecommendationEngine, RECOMMENDATIONS
from moodlens.tracker import MoodTracker, MoodEntry
from datetime import datetime
import tempfile
import os


# ─── Recommender Tests ────────────────────────────────────────────────────────

class TestRecommendationEngine:
    def setup_method(self):
        self.engine = RecommendationEngine()

    def test_all_emotions_return_recommendations(self):
        for emotion in ["happy", "sad", "angry", "fear", "surprise", "neutral", "disgust"]:
            rec = self.engine.get(emotion)
            assert rec is not None
            assert rec.emotion == emotion

    def test_unknown_emotion_falls_back_to_neutral(self):
        rec = self.engine.get("confused")
        assert rec.emotion == "neutral"

    def test_recommendation_has_required_fields(self):
        rec = self.engine.get("happy")
        assert len(rec.music_genres) > 0
        assert len(rec.activities) > 0
        assert rec.affirmation
        assert rec.breathing
        assert rec.emoji

    def test_summary_output_is_string(self):
        for emotion in self.engine.all_emotions():
            rec = self.engine.get(emotion)
            summary = rec.summary()
            assert isinstance(summary, str)
            assert emotion.upper() in summary

    def test_case_insensitive_lookup(self):
        rec1 = self.engine.get("HAPPY")
        rec2 = self.engine.get("happy")
        assert rec1.emotion == rec2.emotion


# ─── Tracker Tests ────────────────────────────────────────────────────────────

class TestMoodTracker:
    def setup_method(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tracker = MoodTracker(log_path=self.tmp.name)

    def teardown_method(self):
        os.unlink(self.tmp.name)

    def test_log_saves_entry(self):
        self.tracker.log("happy", 0.92, "test-session")
        assert len(self.tracker.entries) == 1
        assert self.tracker.entries[0].emotion == "happy"

    def test_today_summary_reflects_logs(self):
        self.tracker.log("sad", 0.75, "s1")
        self.tracker.log("sad", 0.80, "s1")
        self.tracker.log("happy", 0.60, "s1")
        summary = self.tracker.today_summary()
        assert summary["dominant_mood"] == "sad"
        assert summary["total_readings"] == 3

    def test_weekly_trend_has_7_days(self):
        trend = self.tracker.weekly_trend()
        assert len(trend) == 7

    def test_export_csv_creates_file(self):
        self.tracker.log("neutral", 0.5, "s1")
        out = "/tmp/moodlens_test_export.csv"
        self.tracker.export_csv(out)
        assert os.path.exists(out)
        os.unlink(out)

    def test_persistence_across_instances(self):
        self.tracker.log("angry", 0.88, "persist-test")
        # New instance reading same file
        tracker2 = MoodTracker(log_path=self.tmp.name)
        assert len(tracker2.entries) == 1
        assert tracker2.entries[0].emotion == "angry"

    def test_clear_removes_all_entries(self):
        self.tracker.log("happy", 0.9, "s1")
        self.tracker.clear()
        assert len(self.tracker.entries) == 0


# ─── Detector Shape Test (no camera needed) ──────────────────────────────────

class TestEmotionDetectorAnnotation:
    def test_annotate_frame_returns_same_shape(self):
        from moodlens.detector import EmotionDetector
        detector = EmotionDetector()
        fake_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        analysis = {
            "dominant": "happy",
            "scores": {"happy": 85.0, "neutral": 10.0, "sad": 5.0},
            "region": {"x": 100, "y": 80, "w": 120, "h": 120},
        }
        annotated = detector.annotate_frame(fake_frame, analysis)
        assert annotated.shape == fake_frame.shape
