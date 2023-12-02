from app.ml_model import Model
import app.constant as constant
import logging

# Set up a logger with basic configuration
logging.basicConfig(level=logging.INFO)

emotion_classifier = Model(constant.EMOTION_MODEL).get_pipeline("text-classification")
def get_label_from_score(scores:list[str], labels:list[str]):
    max_score = max(scores)
    ind = scores.index(max_score)
    label = labels[ind]
    return label

def predict_emotions(msg: str):
    emotion = emotion_classifier(msg)
    label = emotion[0]['label']
    return label
