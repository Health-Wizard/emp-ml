from app.constant import HAPPINESS_LABEL, LABEL_SCORES, SENTIMENT_LABELS, WEEKDAY_LABELS, WEEKDAY
import app.schema as schema
import pandas as pd
import datetime
from app.models import HealthData

startDate = datetime.datetime.utcnow()
endDate = startDate-datetime.timedelta(7)


def calculate_health_score(emotions: list[str]):
    positivity_score = 0
    stress_score = 0
    depress_score = 0
    total_score = len(emotions)
    for emotion in emotions:
        score = LABEL_SCORES[emotion]
        positivity_score = positivity_score + score
        stress_score = stress_score + (10 - score)
        if score <= 4:
            depress_score = depress_score + 5
    possitivity_rate = (positivity_score/(total_score*10))
    stress_from_emotions = stress_score / (total_score * 10)

    stress_from_depression = depress_score / (total_score * 5)
    stress_level = 0.6 * stress_from_emotions + 0.3 * stress_from_depression
    return possitivity_rate, stress_level


def calculate_admin_graph(emp_data):
    avg_happiness_index = emp_data['happiness_index'].mean()
    avg_stress_level = emp_data['stree_label'].mean()
    happiness_level = emp_data['happiness_level'].value_counts()
    only_emp_data = emp_data[emp_data['role'] == 'employee']
    stress_by_dept = only_emp_data.groupby('department')['stree_label'].mean()
    only_admin = (emp_data[emp_data['role'] == 'admin']['empId']).tolist()
    admin_health_data = []

    for admin in only_admin:
        healthData = {
            'data':   [schema.AnalyticsData(
                title="Happiness Index",
                data=[avg_happiness_index],
                range=[0, 1],
                graph_type="progress bar"
            ).model_dump(),
                schema.AnalyticsData(
                title="Stress Level",
                data=[avg_stress_level],
                range=[0, 1],
                graph_type="progress bar"
            ).model_dump(),
                schema.AnalyticsData(
                title="Happiness Level",
                data=[happiness_level.values.tolist()],
                label=[happiness_level.index.tolist()],
                range=[0, 1],
                graph_type="pie graph"
            ).model_dump(),
                schema.AnalyticsData(
                title="Stress by Department",
                data=[stress_by_dept.values.tolist()],
                label=[stress_by_dept.index.tolist()],
                range=[0, 1],
                graph_type="bar graph"
            ).model_dump(),
            ]
        }
        admin_health_data.append(
            HealthData(
                empId=int(admin),
                startDate=startDate.isoformat(),
                endDate=endDate.isoformat(),
                health_data=healthData
            )
        )
    return admin_health_data


def calculate_health_index(messages, emp_details):
    health_data = []

    emp_data = pd.DataFrame(emp_details, columns=[
                            'empId', 'companyEmail', 'role', 'department'])
    emp_data['happiness_index'] = [0.0]*len(emp_data)
    emp_data['stree_label'] = [0.0]*len(emp_data)
    only_admin = set((emp_data[emp_data['role'] == 'admin']['companyEmail']).tolist())

    # messages_details = pd.DataFrame.from_dict(messages)

    messages_details = pd.read_csv('fake.csv')
    emp_msg_data = pd.merge(emp_data, messages_details,
                            on='companyEmail', how='inner')

    msg_groupby_user = emp_msg_data.groupby('companyEmail')
    for user_id, msges_data in msg_groupby_user:
        if user_id in only_admin:
            continue
        emotions = msges_data['label']
        msges_data.sort_values(by='day_of_week', inplace=True)
        possitivity_rate, stress_level = calculate_health_score(emotions)
        emotions_group = msges_data['label'].value_counts()
        sentiment_group = msges_data['sentiment'].value_counts().reindex(
            SENTIMENT_LABELS, fill_value=0)
        sentiments_per_day = msges_data.groupby('day_of_week')['sentiment'].value_counts(
        ).unstack(fill_value=0).reindex(WEEKDAY_LABELS, fill_value=0).sort_index()
        # Count of emotions per day
        neg_data = msges_data[msges_data['sentiment'] == 'negative']
        negative_emotions_per_day = neg_data.groupby('day_of_week')['label'].value_counts(
        ).unstack(fill_value=0).reindex(WEEKDAY_LABELS, fill_value=0).sort_index()
        emp_data.loc[emp_data['companyEmail'] == str(
            user_id), 'happiness_index'] = possitivity_rate
        emp_data.loc[emp_data['companyEmail'] == str(
            user_id), 'stree_label'] = stress_level

        healthdata = {
            'data':  [schema.AnalyticsData(
                title="Happiness Level of Employee",
                data=[possitivity_rate],
                range=[0, 1],
                graph_type="progress bar"
            ).model_dump(),
                schema.AnalyticsData(
                title="Stress Level of Employee",
                data=[stress_level],
                range=[0, 1],
                graph_type="progress bar"
            ).model_dump(),
                schema.AnalyticsData(
                title="Mood Graph of Employee",
                data=[emotions_group.values.tolist()],
                label=[emotions_group.index.tolist()],
                range=[0, 1],
                graph_type="pie graph"
            ).model_dump(),
                schema.AnalyticsData(
                title="Weekly Sentiments",
                data=sentiments_per_day.values.tolist(),
                label=sentiments_per_day.columns.tolist(),
                xrange=WEEKDAY,
                graph_type="bar graph"
            ).model_dump(),
                schema.AnalyticsData(
                title="Weekly Negative Emotions",
                data=negative_emotions_per_day.values.tolist(),
                label=negative_emotions_per_day.columns.tolist(),
                xrange=WEEKDAY,
                graph_type="bar graph"
            ).model_dump()
            ]

        }
        health_data.append(
            HealthData(
                empId=int(msges_data['empId'].tolist()[0]),
                startDate=startDate.isoformat(),
                endDate=endDate.isoformat(),
                health_data=healthdata)
        )
    emp_data['happiness_level'] = emp_data['happiness_index'].apply(
        lambda x: HAPPINESS_LABEL[0] if x > 6 else HAPPINESS_LABEL[1] if x >= 4 and x <= 6 else HAPPINESS_LABEL[2])
    admin_health_data = calculate_admin_graph(emp_data)
    health_data.extend(admin_health_data)
    return health_data
