# 🎭 MoodLens

> **Real-time facial emotion detection + personalized music, activity & wellness recommendations — all from your webcam.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DeepFace](https://img.shields.io/badge/Powered%20by-DeepFace-orange)](https://github.com/serengil/deepface)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.9%2B-red?logo=opencv)](https://opencv.org)

---

## ✨ What is MoodLens?

MoodLens is a Python AI project that uses your **webcam** to detect your facial emotion in real-time and instantly suggest:

- 🎵 **Music genres** that match or uplift your mood
- ⚡ **Activities** tailored to your emotional state
- 💬 **Affirmations** to keep you grounded
- 🌬 **Breathing exercises** calibrated to your mood
- 📊 **Daily & weekly mood history** with a built-in tracker

It detects 7 emotions — `happy`, `sad`, `angry`, `fear`, `surprise`, `disgust`, `neutral` — using **DeepFace** (built on TensorFlow) and overlays confidence bars on a live OpenCV video stream.

---

## 🚀 Demo

```
─────────────────────────────────────────────────
😊  Mood: HAPPY
🎵  Music:    Afrobeats
⚡  Activity: Start a new project
💬  Reminder: Your energy is contagious — keep shining!
🌬  Breathe:  Box breath: inhale 4s → hold 4s → exhale 4s → hold 4s
─────────────────────────────────────────────────
```

---

## 🗂 Project Structure

```
MoodLens/
├── main.py                  # Entry point (CLI)
├── moodlens/
│   ├── __init__.py
│   ├── detector.py          # Face detection + DeepFace emotion analysis
│   ├── recommender.py       # Emotion → recommendation mapping engine
│   └── tracker.py           # Mood history logger + analytics
├── tests/
│   └── test_moodlens.py     # Unit tests (pytest)
├── requirements.txt
├── setup.py
├── LICENSE
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repo

```bash
git clone https://github.com/your-username/MoodLens.git
cd MoodLens
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** DeepFace will automatically download the emotion model (~80MB) on first run.

---

## 🖥 Usage

### Live webcam mode (default)

```bash
python main.py live
```

| Key | Action |
|-----|--------|
| `Q` | Quit |
| `S` | Print today's mood summary |

### Analyze a single image

```bash
python main.py image path/to/photo.jpg
```

Saves an annotated version as `output_annotated.jpg`.

### View mood history

```bash
python main.py summary
python main.py summary --export     # also exports mood_export.csv
```

### Options

```bash
python main.py live --camera 1       # use secondary camera
python main.py live --interval 3.0   # analyze every 3 seconds
python main.py live --no-log         # disable mood logging
```

---

## 🧠 How It Works

```
Webcam Frame
     │
     ▼
OpenCV Face Detection (Haar Cascade)
     │
     ▼
DeepFace Emotion Analysis (every N seconds)
     │
     ├──► 7 emotion scores (happy, sad, angry, fear, surprise, disgust, neutral)
     │
     ▼
Recommendation Engine
     │
     ├──► Music genre suggestion
     ├──► Activity suggestion
     ├──► Affirmation
     └──► Breathing exercise
     │
     ▼
MoodTracker (JSON log)
     │
     └──► Daily summary + weekly trend
```

---

## 📊 Supported Emotions & Recommendations

| Emotion   | Music Example        | Activity Example       | Breathing Technique              |
|-----------|----------------------|------------------------|----------------------------------|
| 😊 Happy   | Afrobeats, Funk      | Call a friend          | Box breathing (4-4-4-4)          |
| 😢 Sad     | Lo-fi, Ambient       | Journal your thoughts  | 4-7-8 technique                  |
| 😠 Angry   | Hard Rock, Rap       | Go for a run           | Physiological sigh               |
| 😨 Fear    | Binaural Beats       | 5-4-3-2-1 grounding    | Extended exhale (4s in / 8s out) |
| 😲 Surprise| Jazz Fusion, World   | Explore something new  | Equal breathing (5-5)            |
| 😐 Neutral | Lo-fi Study Beats    | Meditate for 5 mins    | Coherent breathing               |
| 🤢 Disgust | Smooth Jazz, R&B     | Clean your space       | Belly breathing                  |

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

Tests cover:
- Recommendation engine for all 7 emotions
- Edge cases (unknown emotion fallback, case-insensitivity)
- MoodTracker persistence, CSV export, weekly trend
- Frame annotation shape preservation

---

## 🔧 Requirements

- Python 3.10+
- Webcam (for live mode)
- ~500MB disk space (TensorFlow + DeepFace model weights)

| Package | Version |
|---------|---------|
| opencv-python | ≥ 4.9.0 |
| deepface | ≥ 0.0.93 |
| tensorflow | ≥ 2.16.0 |
| numpy | ≥ 1.26.0 |
| pytest | ≥ 8.0.0 |

---

## 🌱 Roadmap / Ideas to Extend

- [ ] Spotify API integration — auto-play music matching mood
- [ ] Streamlit or Gradio web dashboard
- [ ] Multi-face detection in group settings
- [ ] Voice-based emotion detection (audio + video fusion)
- [ ] Mood-based notification system
- [ ] Mobile app via Kivy or BeeWare

---

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you'd like to change.

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/add-spotify`
3. Commit your changes: `git commit -m "Add Spotify integration"`
4. Push: `git push origin feature/add-spotify`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [DeepFace](https://github.com/serengil/deepface) by Sefik Ilkin Serengil
- [OpenCV](https://opencv.org/) community
- TensorFlow / Keras emotion model

---

*Built with 💙 using Python, OpenCV, and DeepFace*
