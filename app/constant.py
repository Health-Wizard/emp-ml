CLASSIFICATION_MODEL = "app/model/MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
EMOTION_MODEL = "app/model/SamLowe/roberta-base-go_emotions"

SENTIMENT_LABELS = ["Positive", "Negative", "Neutral"]
WEEKDAY = ['Monday', 'Tuesday', 'Wednesday',
           'Thursday', 'Friday', 'Saturday', 'Sunday']
WEEKDAY_LABELS = [x for x in range(7)]

HAPPINESS_LABEL = [
    'Good',
    'Neutral',
    'Critical'
]

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
