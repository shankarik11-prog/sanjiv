"""
MoodLens - Main Entry Point
Run: python main.py
"""

import cv2
import uuid
import time
import argparse
from moodlens.detector import EmotionDetector
from moodlens.recommender import RecommendationEngine
from moodlens.tracker import MoodTracker


def run_live(camera_index: int = 0, interval: float = 2.0, save_log: bool = True):
    """
    Launch real-time webcam mood detection loop.

    Args:
        camera_index: Webcam index (default 0)
        interval:     Seconds between DeepFace analyses (default 2.0)
        save_log:     Whether to persist mood logs (default True)
    """
    detector = EmotionDetector()
    engine = RecommendationEngine()
    tracker = MoodTracker() if save_log else None
    session_id = str(uuid.uuid4())[:8]

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("❌  Could not open camera. Check your camera index.")
        return

    print("🎭  MoodLens started — press Q to quit, S to see today's summary\n")

    last_analysis_time = 0
    last_analysis = None
    last_emotion = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        now = time.time()

        # Run DeepFace analysis every `interval` seconds
        if now - last_analysis_time >= interval:
            analysis = detector.analyze_emotion(frame)
            if analysis:
                last_analysis = analysis
                last_emotion = analysis["dominant"]
                confidence = analysis["scores"].get(last_emotion, 0)

                rec = engine.get(last_emotion)
                print("\n" + "─" * 50)
                print(rec.summary())
                print("─" * 50)

                if tracker:
                    tracker.log(last_emotion, confidence, session_id)

            last_analysis_time = now

        # Annotate frame
        display = frame.copy()
        if last_analysis:
            display = detector.annotate_frame(display, last_analysis)

        cv2.putText(
            display, "MoodLens | Press Q to quit",
            (10, display.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1
        )
        cv2.imshow("MoodLens", display)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("s") and tracker:
            summary = tracker.today_summary()
            print("\n📊 Today's Summary:", summary)

    cap.release()
    cv2.destroyAllWindows()

    if tracker:
        trend = tracker.weekly_trend()
        print("\n📈 Weekly Mood Trend:")
        for day in trend:
            print(f"  {day['date']}: {day['dominant']} ({day['readings']} readings)")


def run_image(image_path: str):
    """Analyze a single image file."""
    detector = EmotionDetector()
    engine = RecommendationEngine()

    frame = cv2.imread(image_path)
    if frame is None:
        print(f"❌  Could not load image: {image_path}")
        return

    analysis = detector.analyze_emotion(frame)
    if analysis:
        rec = engine.get(analysis["dominant"])
        print(rec.summary())
        annotated = detector.annotate_frame(frame, analysis)
        out_path = "output_annotated.jpg"
        cv2.imwrite(out_path, annotated)
        print(f"\n✅  Annotated image saved → {out_path}")
    else:
        print("😶  No face detected in the image.")


def main():
    parser = argparse.ArgumentParser(
        description="MoodLens — Real-time Facial Emotion Analyzer & Recommender"
    )
    subparsers = parser.add_subparsers(dest="command")

    # live command
    live_parser = subparsers.add_parser("live", help="Run live webcam detection")
    live_parser.add_argument("--camera", type=int, default=0, help="Camera index (default: 0)")
    live_parser.add_argument("--interval", type=float, default=2.0, help="Analysis interval in seconds")
    live_parser.add_argument("--no-log", action="store_true", help="Disable mood logging")

    # image command
    img_parser = subparsers.add_parser("image", help="Analyze a single image")
    img_parser.add_argument("path", help="Path to image file")

    # summary command
    sum_parser = subparsers.add_parser("summary", help="Show mood history")
    sum_parser.add_argument("--export", action="store_true", help="Export to CSV")

    args = parser.parse_args()

    if args.command == "live" or args.command is None:
        camera = getattr(args, "camera", 0)
        interval = getattr(args, "interval", 2.0)
        no_log = getattr(args, "no_log", False)
        run_live(camera_index=camera, interval=interval, save_log=not no_log)

    elif args.command == "image":
        run_image(args.path)

    elif args.command == "summary":
        tracker = MoodTracker()
        print("📊 Today:", tracker.today_summary())
        print("\n📈 Weekly Trend:")
        for day in tracker.weekly_trend():
            print(f"  {day['date']}: {day['dominant']} ({day['readings']} readings)")
        if args.export:
            path = tracker.export_csv()
            print(f"\n✅  Exported to {path}")


if __name__ == "__main__":
    main()
