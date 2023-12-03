import re
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.constant import LABEL_SCORES, SENTIMENT_LABELS,EMOTION_MODEL
from app.config import env_config
from app.AI_model import AIModel
import datetime
import logging

# Set up a logger with basic configuration
logging.basicConfig(level=logging.INFO)


client = WebClient(token=env_config.TOKEN)
classifier = AIModel(EMOTION_MODEL).get_pipeline("text-classification")

def predict_emotions(msg: str):
    emotion = classifier(msg)
    label = emotion[0]['label']
    return label

def fetch_channel_details():
    channel_details = client.conversations_list()
    return channel_details['channels']

def filter_channel():
    channels = fetch_channel_details()
    channel_details = []
    for channel in channels:
        channel_details.append(
            {
                'name':channel['name'],
                'channel_id':channel['id'],
                'created_timestamp': float(channel['created'])
            }
        )
    return channel_details


def fetch_user_details(user_id):
    user_info = client.users_info(user=user_id)['user']
    email = user_info['profile']['email']
    return email


def change_timestamp_to_utc(ts):
    utc_time = datetime.datetime.utcfromtimestamp(float(ts))
    return utc_time

def contains_only_special_chars(sentence):
    if bool(re.match(r'^\S+$', sentence)):
        return True
    elif bool(re.match(r'^[^\w\s]+(\s[^\w\s]+)*$', sentence)):
        return True
    elif bool(re.match(r'^[\d\s]+$', sentence)):
        return True
    else:
        return False

def filter_messages(messages_details,last_message_id):
    messages = []
    pattern = r'.*has joined the channel.*'
    for msg in messages_details:
        text = remove_punctuation_numbers_special_chars(msg['text'])
        if not re.search(pattern, text) and text and len(text) <= 500:
            if not last_message_id:
                last_message_id = msg['client_msg_id']
            label = ''
            if contains_only_special_chars(text.strip()):
                continue
            else:
                label = predict_emotions(text)
            logging.info(f"text: '{text}' - {label}")
            score = LABEL_SCORES[label]
            sentiment = None
            if score > 6:
                sentiment = SENTIMENT_LABELS[0]
            elif score < 4:
                sentiment = SENTIMENT_LABELS[1]
            else:
                sentiment = SENTIMENT_LABELS[2]
            timestamp = change_timestamp_to_utc(msg['ts'])
            message = {
                'text': text,
                'timestamp': timestamp,
                'companyEmail': fetch_user_details(msg['user']),
                'day_of_week': timestamp.weekday(),
                'label': label,
                'sentiment': sentiment,
            }
            messages.append(message)
            
    logging.info("messages filtered")
    return messages,last_message_id


def fetch_conversations():
    channels = filter_channel()
    
    messages = []
    for index, channel in enumerate(channels):
        cursor = None
        last_message_id = ''
        try:
            while True:
                msg_details = client.conversations_history(
                    channel=channel['channel_id'], limit=200, cursor=cursor)
                logging.info(f"messages fetched from {channel['name']}")
                channel_msg,last_message_id = filter_messages(msg_details['messages'],last_message_id)
                messages.extend(channel_msg)
                if not msg_details['has_more']:
                    break
                cursor = msg_details['response_metadata'].get('next_cursor')
            if last_message_id:
                channels[index]['last_message_id'] = last_message_id
        except SlackApiError as err:
            channels.pop(index)
            logging.error(err)
           
    return messages,channels


def remove_punctuation_numbers_special_chars(text) -> str:
    # Replace URLs with an empty string
    text_no_links = re.sub(r'https?://\S+|www\.\S+', '', str(text))

    remove_code_block = re.sub(
        r'```.*?```', '', text_no_links, flags=re.DOTALL)
    
    replace_mentions = re.sub(r'<[^>]+>', 'user', remove_code_block)

    # Replace mentions with an empty string
    text_no_mentions = re.sub(r'[@#]', '', replace_mentions)

    # remove unecessary words
    clean_word = re.sub(r'\b\w{25,}\b', '', text_no_mentions)

    keep_characters = r"'\.,\?! "
    # Keep basic punctuation and remove special characters
    text_no_punct = re.sub(f"[^{keep_characters}a-zA-Z0-9]", '', clean_word)

    # Remove extra dots in between sentences
    text_no_extra_dots = re.sub(r'\.(?=\.)', '', text_no_punct)

    clean_extra_space_text = re.sub(r'\s+', ' ', text_no_extra_dots)
    return clean_extra_space_text
