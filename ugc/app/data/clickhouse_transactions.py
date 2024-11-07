import clickhouse_connect
import time
import pandas as pd

client = clickhouse_connect.get_client(
    host="localhost", port=8123, username="default", password=""
)


def select_all_data():
    return "SELECT * FROM user_activity_analytics;"


def filter_by_event_type():
    return "SELECT * FROM user_activity_analytics WHERE event_type = 'video_completed';"


def date_range_query():
    return "SELECT * FROM user_activity_analytics WHERE event_date BETWEEN '2023-01-01' AND '2023-01-31';"


def count_events_by_type():
    return "SELECT event_type, COUNT(*) AS event_count FROM user_activity_analytics GROUP BY event_type;"


def average_duration_by_event_type():
    return "SELECT event_type, AVG(avg_duration) AS average_duration FROM user_activity_analytics GROUP BY event_type;"


def daily_event_count():
    return "SELECT event_date, COUNT(*) AS total_events FROM user_activity_analytics GROUP BY event_date ORDER BY event_date;"


def hourly_aggregation_by_event_type():
    return """
        SELECT event_date, event_hour, event_type, 
               SUM(total_events) AS total_events, AVG(avg_duration) AS average_duration
        FROM user_activity_analytics GROUP BY event_date, event_hour, event_type
        ORDER BY event_date, event_hour;
    """


def most_frequent_page_urls():
    return """
        SELECT page_url, COUNT(*) AS visit_count 
        FROM user_activity_analytics WHERE event_type = 'user_page_click'
        GROUP BY page_url ORDER BY visit_count DESC LIMIT 10;
    """


def percentage_distribution_of_event_types():
    return """
        SELECT event_type, COUNT(*) * 100.0 / (SELECT COUNT(*) 
        FROM user_activity_analytics) AS percentage
        FROM user_activity_analytics GROUP BY event_type;
    """


def rolling_average_of_clicks_over_time():
    return """
        SELECT event_date, 
               AVG(total_clicks) OVER (ORDER BY event_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) 
               AS rolling_avg_clicks FROM user_activity_analytics ORDER BY event_date;
    """


query_functions = {
    "Select All Data": select_all_data,
    "Filter by Event Type": filter_by_event_type,
    "Date Range Query": date_range_query,
    "Count Events by Type": count_events_by_type,
    "Average Duration by Event Type": average_duration_by_event_type,
    "Daily Event Count": daily_event_count,
    "Hourly Aggregation by Event Type": hourly_aggregation_by_event_type,
    "Most Frequent Page URLs": most_frequent_page_urls,
    "Percentage Distribution of Event Types": percentage_distribution_of_event_types,
    "Rolling Average of Clicks Over Time": rolling_average_of_clicks_over_time,
}

results = []


def execute_and_measure(query_name, query_func):
    try:
        query = query_func()
        start_time = time.time()
        result = client.command(query)
        execution_time = time.time() - start_time
        results.append(
            {
                "Query Name": query_name,
                "Execution Time (s)": execution_time,
                "Result Rows": len(result) if result else 0,
                "Status": "Success",
                "Error": None,
            }
        )
    except Exception as e:
        results.append(
            {
                "Query Name": query_name,
                "Execution Time (s)": None,
                "Result Rows": 0,
                "Status": "Failed",
                "Error": str(e),
            }
        )


for query_name, query_func in query_functions.items():
    print(f"Running query: {query_name}")
    execute_and_measure(query_name, query_func)

df_results = pd.DataFrame(results)
df_results.to_csv("clickhouse_query_results.csv", index=False)

print(df_results)
