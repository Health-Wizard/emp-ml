import app.constant as constant
import app.schema as schema
from collections import Counter


def calculate_health_score(emotions: list[str]):
    positivity_score = 0
    stress_score = 0
    depress_score = 0
    total_score = len(emotions)
    for emotion in emotions:
        score = constant.LABEL_SCORES[emotion]
        positivity_score = positivity_score + score
        stress_score = stress_score + (10 - score)
        if score <= 4:
            depress_score = depress_score + 5
    possitivity_rate = (positivity_score/(total_score*10))
    stress_from_emotions = stress_score / (total_score * 10)

    stress_from_depression = depress_score / (total_score * 5)
    stress_level = 0.6 * stress_from_emotions + 0.3 * stress_from_depression
    return possitivity_rate,stress_level




def calculate_health_index(data):
    emotions = data['label']
    possitivity_rate,stress_level = calculate_health_score(emotions)
    print(data['sentiment'].value_counts())
    emotion_distribution = data.groupby(['day_of_week', 'sentiment']).size().unstack().fillna(0)
    positive_counts = []
    negative_counts= []
    neutral_counts  =[]
    if 'positive' in emotion_distribution.columns:
        positive_counts = emotion_distribution['positive'].values.tolist()       
    if 'negative' in emotion_distribution.columns:
        negative_counts = emotion_distribution['negative'].values.tolist()
    if 'neutral' in emotion_distribution.columns:
        neutral_counts = emotion_distribution['neutral'].values.tolist()
    health_data = [schema.AnalyticsData(
        title="Happiness Level of Employee",
        data=[possitivity_rate],
        range=[0, 1],
        graph_type="progress bar"
    ),
        schema.AnalyticsData(
        title="Stress Level of Employee",
        data=[stress_level],
        range=[0, 1],
        graph_type="progress bar"
    ),
        schema.AnalyticsData(
        title="Mood Graph of Employee",
        data=[dict(Counter(emotions))],
        range=[0, len(emotions)],
        graph_type="pie graph"
    ),
        schema.AnalyticsData(
        title="Overall Sentiment of Employee",
        data=[sum(positive_counts), sum(negative_counts),sum(neutral_counts)],
        label = ["Postive", "Negative", "Neutral"],
        range=[0, len(emotions)],
        graph_type="pie graph"
    ),
     schema.AnalyticsData(
        title="Sentiment Distribution of Employee over a week",
        data=[positive_counts,negative_counts,neutral_counts],
        label = ["Postive", "Negative", "Neutral"],
        xlabel = [emotion_distribution.index],
        graph_type="bar graph"
    )
    ]
    return health_data
