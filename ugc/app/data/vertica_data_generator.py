import random
from datetime import datetime
from faker import Faker
import vertica_python
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

conn_info = {
    'host': '127.0.0.1',
    'port': 5433,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    'autocommit': True,
}

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
        total_clicks = random.randint(1, 50)
    elif event_type == "page_time_spend":
        avg_duration = random.randint(1, 500)
        total_clicks = 0
    elif event_type == "user_page_click":
        avg_duration = 0
        total_clicks = random.randint(1, 50)

    return (
        event_date,
        event_hour,
        event_type,
        page_url,
        total_events,
        avg_duration,
        total_clicks,
    )

def insert_data_batch(batch_size=BATCH_SIZE):
    batch = [generate_aggregated_data() for _ in range(batch_size)]
    
    with vertica_python.connect(**conn_info) as connection:
        cursor = connection.cursor()
        cursor.executemany("""
            INSERT INTO user_activity_analytics
            (event_date, event_hour, event_type, page_url, total_events, avg_duration, total_clicks)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, batch)
        print(f"Inserted {batch_size} records into Vertica.")

@timer_decorator
def generate_and_insert_data(num_batches):
    for _ in range(num_batches):
        insert_data_batch()

if __name__ == "__main__":
    num_batches = 10000
    generate_and_insert_data(num_batches)
