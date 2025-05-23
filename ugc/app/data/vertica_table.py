import vertica_python

conn_info = {
    "host": "localhost",
    "port": 5444,
    "user": "newdbadmin",
    "password": "vertica",
    "database": "docker",
    "autocommit": True,
}

create_table_query = """
CREATE TABLE IF NOT EXISTS user_activity_analytics (
    event_date DATE,
    event_hour INT,
    event_type VARCHAR(50),
    page_url VARCHAR(255),
    total_events INT,
    avg_duration INT,
    total_clicks INT
);
"""

with vertica_python.connect(**conn_info) as connection:
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    print("Table 'user_activity_analytics' created successfully.")
