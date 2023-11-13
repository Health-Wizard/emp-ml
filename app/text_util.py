import re
import datetime
from app.constant import LABEL_SCORES, CHANNEL_TYPE, APP_ID, TOKEN
import requests
from app.model_utils import predict_emotions
import logging
# Set up a logger with basic configuration
logging.basicConfig(level=logging.ERROR)

headers = {
    'Api-Token': TOKEN
}

timestamp = datetime.datetime.utcnow()


def remove_punctuation_numbers_special_chars(text) -> str:
    # Replace URLs with an empty string
    text_no_links = re.sub(r'https?://\S+|www\.\S+', '', str(text))

    # Replace mentions with an empty string
    text_no_mentions = re.sub(r'[@#]', '', text_no_links)

    # remove unecessary words
    clean_word = re.sub(r'\b\w{25,}\b', '', text_no_mentions)

    keep_characters = r"'\.,\?! "
    # Keep basic punctuation and remove special characters
    text_no_punct = re.sub(f"[^{keep_characters}a-zA-Z0-9]", '', clean_word)

    # Remove extra dots in between sentences
    text_no_extra_dots = re.sub(r'\.(?=\.)', '', text_no_punct)

    clean_extra_space_text = re.sub(r'\s+', ' ', text_no_extra_dots)
    return clean_extra_space_text


def change_mili_to_datetime(timestamp_milliseconds: str):
    timestamp_seconds = timestamp_milliseconds / 1000.0
    return datetime.datetime.utcfromtimestamp(timestamp_seconds)


def fetch_channels():
    channel_details = []
    channels_data = requests.get(
        f"https://api-{APP_ID}.sendbird.com/v3/group_channels?limit=100", headers=headers)
    channels_json = channels_data.json()
    if channels_data.status_code == 200:
        logging.info("Channel fetched.")
        for channel in channels_json['channels']:
            if channel['last_message']:
                channel_details.append({
                    'url': channel['channel_url'],
                    'name': channel['name'],
                    'create_timestamp': change_mili_to_datetime(channel['created_at']),
                    'member_count': channel['member_count'],
                    'type': channel['custom_type'],
                    'last_message_id': (channel['last_message'])['message_id']
                })
    else:
        logging.error("Error while fetching channels" + channels_json)
    return channel_details


def fetch_messages(url=None, name=None, message_id=None, prev_id=None):
    msges_data = []
    msg_len = 200
    while msg_len>=200:
        msg_channl = requests.get(
            f"https://api-{APP_ID}.sendbird.com/v3/{CHANNEL_TYPE}/{url}/messages?message_id={message_id}&prev_limit=200&next_limit=0", headers=headers)
        msg_json = msg_channl.json()
        logging.info("Messages fetched " + name)
        if msg_channl.status_code == 200:
            messages = msg_json['messages']
            if not messages:
                return msges_data
            id = 0
            for msg in messages:
                if prev_id == msg:
                    msg_len=0
                    break
                message = remove_punctuation_numbers_special_chars(
                    msg['message'])
                label = predict_emotions(message)
                logging.info("Label prediced: " + label)
                score = LABEL_SCORES[label]
                sentiment = None
                if score > 6:
                    sentiment = 'Positive'
                elif score < 4:
                    sentiment = 'Negative'
                else:
                    sentiment = 'Neutral'
                timestamp = change_mili_to_datetime(msg['created_at'])
                msges_data.append(
                    {
                        'message': message,
                        'timestamp': timestamp,
                        'user_id': msg['user']['user_id'],
                        'label': label,
                        'sentiment': sentiment,
                        'day_of_week': timestamp.weekday()
                    }
                )
                if id == 0:
                    id = msg['message_id']
                msg_len = len(messages)
            message_id = id
        else:
            logging.error("Error while fetching channels" + msg_json)
    return msges_data
