import random
from datetime import datetime
from faker import Faker
import clickhouse_connect
import time
from functools import wraps

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


fake = Faker()

client = clickhouse_connect.get_client(
    host="localhost", port=8123, username="default", password=""
)

BATCH_SIZE = 1000

def generate_aggregated_data():
    event_date = datetime.now().date()
    event_hour = random.randint(0, 23)
    event_type = random.choice(
        [
            "track_events",
            "quality_change",
            "video_completed",
            "search_filter",
            "page_time_spend",
            "user_page_click",
        ]
    )
    page_url = fake.url()
    total_events = random.randint(100, 500)

    if event_type == "track_events":
        avg_duration = random.randint(1, 500)
        total_clicks = 0
    elif event_type == "quality_change":
        avg_duration = 0
        total_clicks = 0
    elif event_type == "video_completed":
        avg_duration = random.randint(60, 7200)
        total_clicks = 0
    elif event_type == "search_filter":
        avg_duration = 0
        total_clicks = random.randint(
            1, 50
        )
    elif event_type == "page_time_spend":
        avg_duration = random.randint(1, 500)
        total_clicks = 0
    elif event_type == "user_page_click":
        avg_duration = 0
        total_clicks = random.randint(1, 50)

    return {
        "event_date": event_date,
        "event_hour": event_hour,
        "event_type": event_type,
        "page_url": page_url,
        "total_events": total_events,
        "avg_duration": avg_duration,
        "total_clicks": total_clicks,
    }


def insert_data_batch(batch_size=BATCH_SIZE):
    batch = [
        (
            item["event_date"],
            item["event_hour"],
            item["event_type"],
            item["page_url"],
            item["total_events"],
            item["avg_duration"],
            item["total_clicks"],
        )
        for item in [generate_aggregated_data() for _ in range(batch_size)]
    ]
    
    client.insert(
        "user_activity_analytics",
        batch,
        column_names=["event_date", "event_hour", "event_type", "page_url", "total_events", "avg_duration", "total_clicks"]
    )
    print(f"Inserted {batch_size} records into ClickHouse.")

@timer_decorator
def generate_and_insert_data(num_batches):
    for _ in range(num_batches):
        insert_data_batch()


if __name__ == "__main__":
    num_batches = 10000
    generate_and_insert_data(num_batches)
