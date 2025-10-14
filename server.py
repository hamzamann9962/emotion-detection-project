"""
Flask web server for the Emotion Detection application.

Routes:
- "/"                : Renders the UI (templates/index.html).
- "/emotionDetector" : Accepts text and returns a formatted analysis string.
"""
from __future__ import annotations

from typing import Dict, Any

from flask import Flask, render_template, request
from EmotionDetection import emotion_detector

app = Flask(__name__)


def format_sentence(result: Dict[str, Any]) -> str:
    """
    Build the formatted sentence required by the assignment.

    Args:
        result: A dict containing 'anger', 'disgust', 'fear', 'joy', 'sadness',
                and 'dominant_emotion'.

    Returns:
        A human-readable string summarizing the scores and the dominant emotion.
    """
    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


@app.route("/", methods=["GET"])
def home() -> str:
    """Render the main UI page."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET", "POST"])
def emotion_detector_endpoint() -> str:
    """
    Accept text via GET (?textToAnalyze=...) or POST (JSON/form) and return the
    formatted analysis string. For blank input, return a friendly error message.
    """
    if request.method == "GET":
        text = request.args.get("textToAnalyze", default="", type=str)
    else:
        if request.is_json:
            body = request.get_json(silent=True) or {}
            text = str(body.get("textToAnalyze", ""))
        else:
            text = request.form.get("textToAnalyze", default="", type=str)

    result = emotion_detector(text)

    if result.get("dominant_emotion") is None:
        return "Invalid text! Please try again!"

    return format_sentence(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
