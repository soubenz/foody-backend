import json
import time
from datetime import datetime, timedelta
import re
import random
import time


  
def dump_items_to_json(data, restaurant):
    """
    Dump the given data to a JSON file.

    Args:
        data (dict): The data to be dumped to JSON.
        restaurant (str): The name of the restaurant.

    Returns:
        None
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{current_date}_{restaurant}.json"
    with open(filename, 'w') as file:
        json.dump(data, file)


def debug_delay():
    time.sleep(1000)

def slight_delay():
    time.sleep(random.uniform(0.1, 0.5))


def parse_date(date_text):
    """
    Parses the given date text and returns a corresponding datetime object.

    Args:
        date_text (str): The date text to be parsed.

    Returns:
        datetime: The parsed datetime object, or None if the date text is invalid.
    """
    if "ago" in date_text:
        if re.search(r"\d+ day", date_text):
            days_ago = int(re.search(r"\d+", date_text).group())
            date = datetime.now() - timedelta(days=days_ago)
        elif re.search(r"\d+ week", date_text):
            weeks_ago = int(re.search(r"\d+", date_text).group())
            date = datetime.now() - timedelta(weeks=weeks_ago)
        elif re.search(r"a month", date_text):
            date = datetime.now() - timedelta(days=30)
        elif re.search(r"\d+ month", date_text):
            months_ago = int(re.search(r"\d+", date_text).group())
            date = datetime.now() - timedelta(days=months_ago * 30)
        else:
            date = None
    else:
        date = None
    return date



def determine_pricing(text_list):
    """
    Cleans the text inside the list and determines the pricing of the restaurant.

    Args:
        text_list (list): The list containing the text to be cleaned.

    Returns:
        str: The pricing of the restaurant ('affordable', 'moderate', 'expensive').
    """
    cleaned_text = [text.replace('·', '').replace('€', '') for text in text_list]
    num_euros = cleaned_text.count('')
    
    if num_euros == 1:
        return 'affordable'
    elif num_euros == 2:
        return 'moderate'
    elif num_euros > 2:
        return 'expensive'
    else:
        return 'unknown'
