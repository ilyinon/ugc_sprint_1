import argparse
import json
import random
import time
from enum import Enum
from functools import wraps
from uuid import uuid4

import requests
from faker import Faker

fake = Faker()


def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time of {func.__name__}: {execution_time:.6f} seconds")
        return result

    return wrapper


class KafkaTopics(Enum):
    TRACK_EVENTS = "track_events"
    QUALITY_CHANGE = "quality_change"
    VIDEO_COMPLETED = "video_completed"
    SEARCH_FILTER = "search_filter"
    PAGE_TIME_SPEND = "page_time_spend"
    USER_PAGE_CLICK = "user_page_click"


def generate_event_data(event_type):
    """
    Generate a fake data record for a specific event type.
    """
    base_data = {
        "user_id": fake.uuid4(),
        "timestamp": fake.date_time_this_year().isoformat(),
        "event_type": event_type.value,
    }

    if event_type == KafkaTopics.QUALITY_CHANGE:
        old_quality, new_quality = random.sample(
            ["240p", "360p", "480p", "720p", "1080p"], 2
        )
        base_data.update(
            {
                "event_type": KafkaTopics.QUALITY_CHANGE.value,
                "video_id": str(uuid4()),
                "old_quality": old_quality,
                "new_quality": new_quality,
            }
        )
    elif event_type == KafkaTopics.VIDEO_COMPLETED:
        base_data.update({"video_id": str(uuid4), "completed": fake.boolean()})
    elif event_type == KafkaTopics.SEARCH_FILTER:
        base_data.update({"search_term": fake.word(), "filter_applied": fake.boolean()})
    elif event_type == KafkaTopics.PAGE_TIME_SPEND:
        base_data.update(
            {"page_url": fake.url(), "time_spent": fake.random_int(min=1, max=500)}
        )
    elif event_type == KafkaTopics.USER_PAGE_CLICK:
        base_data.update(
            {"page_url": fake.url(), "click_count": fake.random_int(min=1, max=10)}
        )
    else:
        base_data.update(
            {
                "metadata": {
                    "device": fake.user_agent(),
                    "location": {
                        "latitude": fake.latitude(),
                        "longitude": fake.longitude(),
                    },
                }
            }
        )

    return base_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-token", help="Token to access UGC")
    parser.add_argument("-amount", type=int, help="Amount entries to generate")

    args = parser.parse_args()

    count = args.amount
    url = "http://localhost:8010/api/v1/track_event"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {args.token}",
        "Content-Type": "application/json",
    }

    while count > 0:
        data = generate_event_data(KafkaTopics.QUALITY_CHANGE)
        response = requests.post(url, headers=headers, data=json.dumps(data))
        count -= 1

    print(f"Overall {args.amount} requests have been sent to UGC")
