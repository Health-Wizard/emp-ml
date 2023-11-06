import re
import string
from app.constant import CONTRACTION_MAPPING

# Contractions mapping


def expand_contractions(text):
    # Regular expression pattern to find contractions
    pattern = re.compile(
        r'\b(' + '|'.join(CONTRACTION_MAPPING.keys()) + r')\b')

    def expand_match(contraction):
        # print(contraction)
        match = contraction.group(0)
        expanded_contraction = CONTRACTION_MAPPING.get(
            match.lower(), match)
        return expanded_contraction

    # Replace contractions using the mapping
    expanded_text = pattern.sub(expand_match, text)
    return expanded_text


def remove_punctuation_numbers_special_chars(text) -> str:
    # Replace URLs with an empty string
    text_no_links = re.sub(r'https?://\S+|www\.\S+', '', str(text))

    # Replace mentions with an empty string
    text_no_mentions = re.sub(r'[@#]', '', text_no_links)

    # Expand contractions
    expanded_text = expand_contractions(text_no_mentions.lower())

    # remove unecessary words
    clean_word = re.sub(r'\b\w{25,}\b', '', expanded_text)

    keep_characters = r"'\.,\?! "
    # Keep basic punctuation and remove special characters
    text_no_punct = re.sub(f"[^{keep_characters}a-zA-Z0-9]", '', clean_word)

    # Remove extra dots in between sentences
    text_no_extra_dots = re.sub(r'\.(?=\.)', '', text_no_punct)

    clean_extra_space_text = re.sub(r'\s+', ' ', text_no_extra_dots)
    return clean_extra_space_text
