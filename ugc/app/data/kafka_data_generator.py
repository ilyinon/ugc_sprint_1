from decimal import Decimal
import json
import os
import random
from faker import Faker
from kafka import KafkaProducer
from enum import Enum
from core.config import ugc_settings
from data.utils import timer_decorator

class KafkaTopics(Enum):
    TRACK_EVENTS = "track_events"
    QUALITY_CHANGE = "quality_change"
    VIDEO_COMPLETED = "video_completed"
    SEARCH_FILTER = "search_filter"
    PAGE_TIME_SPEND = "page_time_spend"
    USER_PAGE_CLICK = "user_page_click"

producer = KafkaProducer(
    bootstrap_servers=ugc_settings.kafka_bootsrap,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

fake = Faker()

BATCH_SIZE = 1000

def convert_to_serializable(obj):
    """Convert Decimal and other non-serializable types to JSON serializable types."""
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [convert_to_serializable(i) for i in obj]
    return obj

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
        base_data.update({"quality_level": fake.random_element(elements=("240p", "360p", "480p", "720p", "1080p"))})
    elif event_type == KafkaTopics.VIDEO_COMPLETED:
        base_data.update({"video_duration": fake.random_int(min=60, max=7200), "completed": fake.boolean()})
    elif event_type == KafkaTopics.SEARCH_FILTER:
        base_data.update({"search_term": fake.word(), "filter_applied": fake.boolean()})
    elif event_type == KafkaTopics.PAGE_TIME_SPEND:
        base_data.update({"page_url": fake.url(), "time_spent": fake.random_int(min=1, max=500)})
    elif event_type == KafkaTopics.USER_PAGE_CLICK:
        base_data.update({"page_url": fake.url(), "click_count": fake.random_int(min=1, max=10)})
    else:
        base_data.update({"metadata": {"device": fake.user_agent(), "location": {"latitude": fake.latitude(), "longitude": fake.longitude()}}})
    
    return base_data

def generate_data_batch(batch_size=BATCH_SIZE):
    """
    Generator function that yields a batch of fake data records for each event type.
    """
    while True:
        batch = []
        for _ in range(batch_size):
            event_type = random.choice(list(KafkaTopics))
            record = generate_event_data(event_type)
            batch.append((event_type.value, convert_to_serializable(record)))  # Ensure record is serializable
        yield batch

def send_data_to_kafka(batch):
    """
    Sends a batch of records to the appropriate Kafka topic.
    """
    for topic, record in batch:
        producer.send(topic, record)
    producer.flush()
    print(f"Sent batch of {len(batch)} records to Kafka.")

@timer_decorator
def generate_and_send_data(num_batches, batch_size=BATCH_SIZE):
    """
    Generates and sends data in batches to Kafka.
    """
    data_generator = generate_data_batch(batch_size=batch_size)
    for _ in range(num_batches):
        batch = next(data_generator)
        send_data_to_kafka(batch)

if __name__ == "__main__":
    num_batches_to_send = 10000
    generate_and_send_data(num_batches=num_batches_to_send)



# import json
# import os
# import asyncio
# from faker import Faker
# from aiokafka import AIOKafkaProducer

# # Configure constants
# TOPIC_NAME = "topic_name"
# BATCH_SIZE = 1000
# TOTAL_RECORDS = 10_000_000
# NUM_WORKERS = 8

# fake = Faker()

# async def generate_data_batch(batch_size=BATCH_SIZE):
#     """
#     Asynchronously generate a batch of fake data records.
#     """
#     return [
#         {
#             "user_id": fake.uuid4(),
#             "event_type": fake.random_element(elements=("play", "pause", "stop", "like")),
#             "timestamp": fake.date_time_this_year().isoformat(),
#             "metadata": {
#                 "ip_address": fake.ipv4(),
#                 "device": fake.user_agent(),
#                 "location": {
#                     "latitude": fake.latitude(),
#                     "longitude": fake.longitude()
#                 }
#             }
#         }
#         for _ in range(batch_size)
#     ]

# async def send_data_to_kafka(producer, batch, topic=TOPIC_NAME):
#     """
#     Sends a batch of records to Kafka asynchronously.
#     """
#     for record in batch:
#         await producer.send_and_wait(topic, json.dumps(record).encode("utf-8"))

# async def generate_and_send_parallel(total_records=TOTAL_RECORDS, batch_size=BATCH_SIZE, num_workers=NUM_WORKERS):
#     """
#     Generates and sends data to Kafka in parallel using asyncio.
#     """
#     producer = AIOKafkaProducer(
#         bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
#     )
    
#     await producer.start()
#     try:
#         total_batches = total_records // batch_size
        
#         for batch_num in range(0, total_batches, num_workers):
#             tasks = [
#                 asyncio.create_task(
#                     send_data_to_kafka(producer, await generate_data_batch(batch_size))
#                 )
#                 for _ in range(min(num_workers, total_batches - batch_num))
#             ]
            
#             await asyncio.gather(*tasks)
#             print(f"Completed {batch_num + len(tasks)}/{total_batches} batches")
#     finally:
#         await producer.stop()

# if __name__ == "__main__":
#     asyncio.run(generate_and_send_parallel())
