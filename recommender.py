"""
MoodLens - Recommendation Engine
Maps detected emotions to curated music genres, activities,
affirmations, and breathing exercises.
"""

import random
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Recommendation:
    emotion: str
    music_genres: list[str]
    activities: list[str]
    affirmation: str
    breathing: str
    color_theme: str
    emoji: str

    def summary(self) -> str:
        genre = random.choice(self.music_genres)
        activity = random.choice(self.activities)
        return (
            f"{self.emoji}  Mood: {self.emotion.upper()}\n"
            f"🎵  Music:    {genre}\n"
            f"⚡  Activity: {activity}\n"
            f"💬  Reminder: {self.affirmation}\n"
            f"🌬  Breathe:  {self.breathing}"
        )


RECOMMENDATIONS: dict[str, Recommendation] = {
    "happy": Recommendation(
        emotion="happy",
        music_genres=["Indie Pop", "Funk", "Afrobeats", "Upbeat Jazz", "Dance Pop"],
        activities=["Go for a walk", "Call a friend", "Start a new project", "Dance session", "Journal your wins"],
        affirmation="Your energy is contagious — keep shining!",
        breathing="Box breath: inhale 4s → hold 4s → exhale 4s → hold 4s",
        color_theme="#FFD700",
        emoji="😊",
    ),
    "sad": Recommendation(
        emotion="sad",
        music_genres=["Lo-fi Hip Hop", "Acoustic Soul", "Ambient", "Classical Piano", "Indie Folk"],
        activities=["Make warm tea", "Watch comfort shows", "Write in a journal", "Take a nap", "Go outside briefly"],
        affirmation="It's okay to feel this way. This too shall pass.",
        breathing="4-7-8: inhale 4s → hold 7s → exhale 8s (repeat 3×)",
        color_theme="#6495ED",
        emoji="😢",
    ),
    "angry": Recommendation(
        emotion="angry",
        music_genres=["Heavy Metal", "Hard Rock", "Drum & Bass", "Intense Classical", "Rap"],
        activities=["Go for a run", "Punch a pillow", "Cold shower", "Write unsent letters", "Do push-ups"],
        affirmation="Pause. Breathe. You are in control of your response.",
        breathing="Physiological sigh: double inhale through nose → long exhale through mouth",
        color_theme="#FF4500",
        emoji="😠",
    ),
    "fear": Recommendation(
        emotion="fear",
        music_genres=["Meditation Music", "Binaural Beats", "Soft Ambient", "Nature Sounds", "Chill Acoustic"],
        activities=["Ground yourself (5-4-3-2-1 senses)", "Call someone you trust", "Tidy your space", "Drink cold water", "Step outside"],
        affirmation="You are safe right now. One step at a time.",
        breathing="Extended exhale: inhale 4s → exhale 8s (activates vagus nerve)",
        color_theme="#9370DB",
        emoji="😨",
    ),
    "surprise": Recommendation(
        emotion="surprise",
        music_genres=["Eclectic Mix", "World Music", "Jazz Fusion", "Experimental", "Cinematic"],
        activities=["Explore something new", "Try a new recipe", "Watch a documentary", "Freewrite for 5 mins", "Sketch or doodle"],
        affirmation="Stay curious — surprises often open new doors.",
        breathing="Equal breathing: inhale 5s → exhale 5s (balances nervous system)",
        color_theme="#FF8C00",
        emoji="😲",
    ),
    "neutral": Recommendation(
        emotion="neutral",
        music_genres=["Background Jazz", "Lo-fi Study Beats", "Chill Electronica", "Soft Classical", "Bossa Nova"],
        activities=["Plan your day", "Learn something new", "Read a book", "Meditate for 5 mins", "Stretch"],
        affirmation="Stillness is underrated — use this calm productively.",
        breathing="Coherent breathing: inhale 5s → exhale 5s at your own pace",
        color_theme="#A9A9A9",
        emoji="😐",
    ),
    "disgust": Recommendation(
        emotion="disgust",
        music_genres=["Uplifting Classical", "Smooth Jazz", "Chill R&B", "Acoustic Pop", "Indie Chill"],
        activities=["Clean your space", "Take a shower", "Go outdoors", "Cook a healthy meal", "Do a creative project"],
        affirmation="Redirect your energy — discomfort often sparks positive change.",
        breathing="Belly breathing: place hand on belly, breathe deep so only belly rises — 5 slow cycles",
        color_theme="#228B22",
        emoji="🤢",
    ),
}


class RecommendationEngine:
    """Maps detected emotion to a curated Recommendation object."""

    def get(self, emotion: str) -> Recommendation:
        emotion = emotion.lower().strip()
        return RECOMMENDATIONS.get(emotion, RECOMMENDATIONS["neutral"])

    def all_emotions(self) -> list[str]:
        return list(RECOMMENDATIONS.keys())
