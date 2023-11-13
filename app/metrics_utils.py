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


def distribution_data_over_week(data, groupby=None):
   distribution_data = data.groupby(groupby).size().unstack().fillna(0)
   return distribution_data.values.tolist(),distribution_data.index


def calculate_health_index(data):
    emotions=data['label']
    data = data.sort_values(by='day_of_week')
    possitivity_rate,stress_level = calculate_health_score(emotions)
    emotions_group = data['label'].value_counts()
    sentiment_group = data['sentiment'].value_counts().reindex(constant.SENTIMENT_LABELS, fill_value=0)
    # Count of sentiment per day
    sentiments_per_day = data.groupby('day_of_week')['sentiment'].value_counts().unstack(fill_value=0).reindex(constant.WEEKDAY_LABELS, fill_value=0).sort_index()
    print(sentiments_per_day)
    # Count of emotions per day
    neg_data = data[data['sentiment'] == 'negative']
    negative_emotions_per_day = neg_data.groupby('day_of_week')['label'].value_counts().unstack(fill_value=0).reindex(constant.WEEKDAY_LABELS, fill_value=0).sort_index()
    print(negative_emotions_per_day)
    # positive_counts = []
    # negative_counts= []
    # neutral_counts  =[]
    # if 'positive' in sent_distribution.columns:
    #     positive_counts = sent_distribution['positive'].values.tolist()       
    # if 'negative' in sent_distribution.columns:
    #     negative_counts = sent_distribution['negative'].values.tolist()
    # if 'neutral' in sent_distribution.columns:
    #     neutral_counts = sent_distribution['neutral'].values.tolist()
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
        data=[emotions_group.values.tolist()],
        label = [emotions_group.index.tolist()],
        range=[0, 1],
        graph_type="pie graph"
    ),
        schema.AnalyticsData(
        title="Overall Sentiment Percentage",
        data=sentiment_group.values.tolist(),
        label = sentiment_group.index.tolist(),
        range=[0, 1],
        graph_type="pie graph"
    ),
     schema.AnalyticsData(
        title="Sentiment Distribution over a week",
        data=sentiments_per_day.values.tolist(),
        label = constant.SENTIMENT_LABELS,
        xrange = constant.WEEKDAY,
        graph_type="bar graph"
    ),
     schema.AnalyticsData(
        title="Negative Emotions Distribution over a week",
        data=negative_emotions_per_day.values.tolist(),
        label = negative_emotions_per_day.columns.tolist(),
        xrange = constant.WEEKDAY,
        graph_type="bar graph"
    )
    ]
    return health_data
