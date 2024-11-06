import json
import random
import time
from datetime import datetime
from enum import Enum
from functools import wraps
from multiprocessing import Pool
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
    num_batches = 10000
    url = "http://localhost:8010/api/v1/track_event"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNDM3MGE5NzgtMmQ5NS00N2VlLThkYTItZmRjMmQ4Y2QxYmI3IiwiZW1haWwiOiJ1c2VyQG1hLmlsIiwicm9sZXMiOiJ1c2VyIiwiZXhwIjoxNzMwOTM3NDU3LCJqdGkiOiJkYjVjMmI2Yy0yOGE3LTRkZTItYjU5Yy02NWJhMjljMWRhYTEifQ.L3k_AEP-T1ImwGMfylfre2OMoRBeqNGYLqneXG4rcWk",
        "Content-Type": "application/json",
    }

    # while num_batches > 0:
    #     data = generate_event_data(KafkaTopics.QUALITY_CHANGE)
    #     response = requests.post(url, headers=headers, data=json.dumps(data))
    #     # print(response.status_code)
    #     num_batches -= 1

    data = generate_event_data(KafkaTopics.QUALITY_CHANGE)
    response = requests.post(url, headers=headers, data=json.dumps(data))
