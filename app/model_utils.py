from app.ml_model import Model
import app.constant as constant
import logging
# Set up a logger with basic configuration
logging.basicConfig(level=logging.INFO)

emotion_classifier = Model(constant.EMOTION_MODEL).get_pipeline("text-classification")
# emotion_label_classifier = Model(constant.CLASSIFICATION_MODEL).get_pipeline('zero-shot-classification')

def get_label_from_score(scores:list[str], labels:list[str]):
    max_score = max(scores)
    ind = scores.index(max_score)
    label = labels[ind]
    return label


# def get_predicted_label(text: str, label :str):
#     result = None
#     if label == 'sadness':
#         result = emotion_label_classifier(text, constant.SAD_LABEL, multi_label=False)
#         logging.info("Sadness label predicted..")
#     elif label == 'happiness':
#         result = emotion_label_classifier(text, constant.HAPPY_LABEL, multi_label=False)
#         logging.info("Happiness label predicted..")
#     elif label == 'disgust':
#         result = emotion_label_classifier(text, constant.DISGRUST_LABEL, multi_label=False)
#         logging.info("Digust label predicted..")
#     elif label == 'anger':
#         result = emotion_label_classifier(text, constant.ANGER_LABEL, multi_label=False)
#         logging.info("Anger label predicted..")
#     elif label == 'fear':
#         result = emotion_label_classifier(text, constant.FEAR_LABEL, multi_label=False)
#         logging.info("Fear label predicted..")
#     elif label == 'surprise':
#         result = emotion_label_classifier(text, constant.SURPRISE_LABEL, multi_label=False)
#         logging.info("Surprise label predicted..")
#     else:
#         result = emotion_label_classifier(text, constant.NEUTRAL_LABEL, multi_label=False)
#         logging.info("Neutral label predicted..")
#     return get_label_from_score(result['scores'], result['labels'])



def predict_emotions(msg: str):
    emotion = emotion_classifier(msg)
    label = emotion[0]['label']
    logging.info(f"Predicted label - {label}")
    return label
