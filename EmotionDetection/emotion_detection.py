import json
import requests

URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

def _empty_result():
    """Return the required dict with None values for invalid/blank input."""
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }

def emotion_detector(text_to_analyze):
    """
    Call Watson EmotionPredict and return the formatted dict.
    """
    if not text_to_analyze or text_to_analyze.strip() == "":
        return _empty_result()

    payload = {"raw_document": {"text": text_to_analyze}}
    try:
        response = requests.post(URL, headers=HEADERS, json=payload, timeout=10)
    except requests.RequestException:
        return _empty_result()

    if response.status_code == 400:
        return _empty_result()
    if response.status_code != 200:
        return _empty_result()

    # Parse JSON
    try:
        data = json.loads(response.text)
        emotions = data["emotionPredictions"][0]["emotion"]
    except (json.JSONDecodeError, KeyError, IndexError):
        return _empty_result()

    anger   = float(emotions.get("anger", 0.0))
    disgust = float(emotions.get("disgust", 0.0))
    fear    = float(emotions.get("fear", 0.0))
    joy     = float(emotions.get("joy", 0.0))
    sadness = float(emotions.get("sadness", 0.0))

    result = {
        "anger": anger,
        "disgust": disgust,
        "fear": fear,
        "joy": joy,
        "sadness": sadness,
    }
    result["dominant_emotion"] = max(result, key=result.get)
    return result
