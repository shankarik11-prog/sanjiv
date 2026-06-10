"""
MoodLens - Mood History Tracker
Logs detected emotions with timestamps, provides daily/weekly
summaries, and exports to CSV.
"""

import csv
import json
from datetime import datetime, timedelta
from collections import Counter
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class MoodEntry:
    timestamp: str
    emotion: str
    confidence: float
    session_id: str

    def to_dict(self) -> dict:
        return asdict(self)


class MoodTracker:
    """
    Persists mood readings to a local JSON log.
    Provides analytics: streaks, dominant moods, trend charts.
    """

    def __init__(self, log_path: str = "mood_log.json"):
        self.log_path = Path(log_path)
        self.entries: list[MoodEntry] = []
        self._load()

    def _load(self):
        if self.log_path.exists():
            try:
                raw = json.loads(self.log_path.read_text())
                self.entries = [MoodEntry(**e) for e in raw]
            except Exception:
                self.entries = []

    def _save(self):
        self.log_path.write_text(
            json.dumps([e.to_dict() for e in self.entries], indent=2)
        )

    def log(self, emotion: str, confidence: float, session_id: str):
        entry = MoodEntry(
            timestamp=datetime.now().isoformat(),
            emotion=emotion.lower(),
            confidence=round(confidence, 2),
            session_id=session_id,
        )
        self.entries.append(entry)
        self._save()

    def today_summary(self) -> dict:
        today = datetime.now().date()
        today_entries = [
            e for e in self.entries
            if datetime.fromisoformat(e.timestamp).date() == today
        ]
        if not today_entries:
            return {"message": "No mood data for today yet."}
        counts = Counter(e.emotion for e in today_entries)
        dominant = counts.most_common(1)[0][0]
        return {
            "date": str(today),
            "total_readings": len(today_entries),
            "dominant_mood": dominant,
            "mood_counts": dict(counts),
            "avg_confidence": round(
                sum(e.confidence for e in today_entries) / len(today_entries), 2
            ),
        }

    def weekly_trend(self) -> list[dict]:
        trend = []
        today = datetime.now().date()
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            day_entries = [
                e for e in self.entries
                if datetime.fromisoformat(e.timestamp).date() == day
            ]
            counts = Counter(e.emotion for e in day_entries)
            dominant = counts.most_common(1)[0][0] if counts else "—"
            trend.append({
                "date": str(day),
                "dominant": dominant,
                "readings": len(day_entries),
            })
        return trend

    def export_csv(self, path: str = "mood_export.csv"):
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "emotion", "confidence", "session_id"])
            writer.writeheader()
            for e in self.entries:
                writer.writerow(e.to_dict())
        return path

    def clear(self):
        self.entries = []
        self._save()
