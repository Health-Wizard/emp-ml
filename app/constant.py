CLASSIFICATION_MODEL = "app/model/MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
PASSWORD = "pioneersp"
DB_URL = f"mongodb+srv://pioneersp:{PASSWORD}@cluster0.rrnp1r4.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "org_details"
CONTRACTION_MAPPING = {
    "ain't": "is not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "could've": "could have",
    "couldn't": "could not",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'll": "he will",
    "he's": "he is",
    "how'd": "how did",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "i would",
    "i'll": "i will",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'll": "it will",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mightn't": "might not",
    "mustn't": "must not",
    "needn't": "need not",
    "oughtn't": "ought not",
    "shan't": "shall not",
    "she'd": "she would",
    "she'll": "she will",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "that's": "that is",
    "there's": "there is",
    "they'd": "they would",
    "they'll": "they will",
    "they're": "they are",
    "they've": "they have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'll": "we will",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "where's": "where is",
    "who'd": "who would",
    "who'll": "who will",
    "who're": "who are",
    "who's": "who is",
    "who've": "who have",
    "won't": "will not",
    "wouldn't": "would not",
    "you'd": "you would",
    "you'll": "you will",
    "you're": "you are",
    "you've": "you have"
}

EMOTION_LABEL = ["sadness", "happiness", "disgust",
                 "anger", "fear", "surprise", "neutral"]
HAPPY_LABEL = [
    "excitement",
    "joy",
    "love",
    "optimism",
    "admiration",
    "gratitude"
]
SAD_LABEL = [
    "grief",
    "disappointment",
    "remorse",
    "sorrow"
]

DISGRUST_LABEL = [
    "repugnance",
    "contempt",
    "disapproval"
]

ANGER_LABEL = ["frustration", "annoyance", "irritation", "aggressive"]

FEAR_LABEL = ["panic", "anxiety", "worry", "nervousness"]

NEUTRAL_LABEL = ["relief",
                 "caring",
                 "approval",
                 "desire",
                 "pride"]

SURPRISE_LABEL = ["amazement", "shock", "confusion"]

LABEL_SCORES = {
    "amazement": 7,
    "admiration": 7,
    "amusement": 8,
    "anger": 2,
    "annoyance": 2,
    "anxiety" : 2,
    "approval": 7,
    "caring": 7,
    "confusion": 4,
    "worry" : 3,
    "curiosity": 6,
    "repugnance": 1,
    "contempt": 2,
    "desire": 6,
    "disappointment": 3,
    "disapproval": 4,
    "disgust": 1,
    "embarrassment": 2,
    "excitement": 8,
    "fear": 0,
    "gratitude": 8,
    "grief": 2,
    "joy": 10,
    "shock":2,
    "love": 10,
    "nervousness": 2,
    "optimism": 8,
    "pride": 8,
    "realization": 5,
    "relief": 6,
    "remorse": 0,
    "sorrow": 0,
    "surprise": 6,
    "frustration": 1,
    "irritation": 3,
    "aggressive": 0,
    "panic" : 1,
    "neutral": 5
}