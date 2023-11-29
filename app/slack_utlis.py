import re
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.constant import LABEL_SCORES, SENTIMENT_LABELS
from app.model_utils import predict_emotions
import datetime
import logging
import os
from dotenv import load_dotenv

# Set up a logger with basic configuration
logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("TOKEN")
client = WebClient(token=TOKEN)


def fetch_channel_details():
    channel_details = client.conversations_list()
    return channel_details['channels']


def fetch_user_details(user_id):
    user_info = client.users_info(user=user_id)['user']
    email = user_info['profile']['email']
    return email


def change_timestamp_to_utc(ts):
    utc_time = datetime.datetime.utcfromtimestamp(float(ts))
    return utc_time


def filter_messages(messages_details):
    messages = []
    pattern = r'.*has joined the channel.*'
    for msg in messages_details:
        text = msg['text']
        if not re.search(pattern, text) and len(text) != 0:
            label = predict_emotions(text)
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
                'text': remove_punctuation_numbers_special_chars(text),
                'timestamp': timestamp,
                'user_id': fetch_user_details(msg['user']),
                'day_of_week': timestamp.weekday(),
                'label': label,
                'sentiment': sentiment,
            }
            messages.append(message)
        logging.info("message filtered")
    return messages


def fetch_conversations():
    cursor = None
    has_more = True
    channels = fetch_channel_details()
    messages = []
    for channel in channels:
        while (has_more):
            msg_details = client.conversations_history(
                channel=channel['id'], limit=200, cursor=cursor)
            logging.info(f"messages fetched from {channel['name']}")
            has_more = msg_details['has_more']
            cursor = msg_details['response_metadata']['next_cursor'] if msg_details['response_metadata'] else None
            channel_msg = filter_messages(msg_details['messages'])
            messages.extend(channel_msg)
    return messages


def remove_punctuation_numbers_special_chars(text) -> str:
    # Replace URLs with an empty string
    text_no_links = re.sub(r'https?://\S+|www\.\S+', '', str(text))

    remove_code_block = re.sub(
        r'```.*?```', '', text_no_links, flags=re.DOTALL)

    # Replace mentions with an empty string
    text_no_mentions = re.sub(r'[@#]', '', remove_code_block)

    # remove unecessary words
    clean_word = re.sub(r'\b\w{25,}\b', '', text_no_mentions)

    keep_characters = r"'\.,\?! "
    # Keep basic punctuation and remove special characters
    text_no_punct = re.sub(f"[^{keep_characters}a-zA-Z0-9]", '', clean_word)

    # Remove extra dots in between sentences
    text_no_extra_dots = re.sub(r'\.(?=\.)', '', text_no_punct)

    clean_extra_space_text = re.sub(r'\s+', ' ', text_no_extra_dots)
    return clean_extra_space_text
