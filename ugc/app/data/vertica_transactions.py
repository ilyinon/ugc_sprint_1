import time

import pandas as pd
import vertica_python

conn_info = {
    "host": "localhost",
    "port": 5444,
    "user": "newdbadmin",
    "password": "vertica",
    "database": "docker",
    "autocommit": True,
}


def select_all_data():
    return "SELECT * FROM user_activity_analytics;"


def filter_by_event_type():
    return "SELECT * FROM user_activity_analytics WHERE event_type = 'video_completed';"


def date_range_query():
    return "SELECT * FROM user_activity_analytics WHERE event_date BETWEEN '2024-01-01' AND '2024-01-31';"


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
        SELECT event_type,
               COUNT(*) * 100.0 / total.total_event_count AS percentage
        FROM user_activity_analytics
        CROSS JOIN (SELECT COUNT(*) AS total_event_count FROM user_activity_analytics) AS total
        GROUP BY event_type, total.total_event_count;
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


def execute_and_measure(query_name, query_func, cursor):
    try:
        query = query_func()
        start_time = time.time()
        cursor.execute(query)
        result = cursor.fetchall()
        execution_time = time.time() - start_time
        results.append(
            {
                "Query Name": query_name,
                "Execution Time (s)": execution_time,
                "Result Rows": len(result),
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


with vertica_python.connect(**conn_info) as connection:
    cursor = connection.cursor()
    for query_name, query_func in query_functions.items():
        print(f"Running query: {query_name}")
        execute_and_measure(query_name, query_func, cursor)

df_results = pd.DataFrame(results)
df_results.to_csv("vertica_query_results.csv", index=False)

print(df_results)
