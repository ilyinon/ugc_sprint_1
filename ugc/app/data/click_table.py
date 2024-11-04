import clickhouse_connect

client = clickhouse_connect.get_client(
    host="localhost", port=8123, username="default", password=""
)

create_table_query = """
CREATE TABLE IF NOT EXISTS user_activity_analytics (
    event_date Date,   
    event_hour UInt8,   
    event_type LowCardinality(String),
    page_url String,        
    total_events UInt32,      
    avg_duration UInt32,             
    total_clicks UInt32
) 
ENGINE = MergeTree()
PARTITION BY event_date
ORDER BY (event_date, event_hour, event_type);
"""

client.command(create_table_query)

print("Table 'user_activity_analytics' created successfully.")
