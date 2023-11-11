CLASSIFICATION_MODEL = "app/model/MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
EMOTION_MODEL = "app/model/SamLowe/roberta-base-go_emotions"
PASSWORD = "pioneersp"
CHANNEL_TYPE = "group_channels"
APP_ID = "8E9DD5B3-51F9-40BF-A851-F639C6C4A888"
TOKEN = "0c3cd6f3ad79ee8c40fe51cad7ede9ae1271b784"
DB_URL = f"mongodb+srv://pioneersp:{PASSWORD}@cluster0.rrnp1r4.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "org_details"


EMOTION_LABEL = ["sadness", "happiness", "disgust",
                 "anger", "fear", "surprise", "neutral"]


LABEL_SCORES = {
    "admiration": 7,
    "amusement": 8,
    "anger": 2,
    "annoyance": 2,
    "approval": 6,
    "caring": 6,
    "confusion": 4,
    "curiosity": 6,
    "desire": 6,
    "realization": 5,
    "disappointment": 3,
    "disapproval": 4,
    "disgust": 1,
    "embarrassment": 2,
    "excitement": 8,
    "fear": 0,
    "gratitude": 8,
    "grief": 2,
    "joy": 10,
    "love": 10,
    "optimism": 8,
    "pride": 7,
    "relief": 6,
    "nervousness": 3,
    "remorse": 0,
    "surprise": 6,
    "sadness": 2,
    "neutral": 5
}
