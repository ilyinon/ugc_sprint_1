
import clickhouse_connect

client = clickhouse_connect.get_client(
    host="localhost", port=8123, username="default", password=""
)

truncate_table_query = "TRUNCATE TABLE user_activity_analytics"

client.command(truncate_table_query)
print("Table 'user_activity_analytics' truncated successfully.")
