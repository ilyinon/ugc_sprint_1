import vertica_python

conn_info = {
    "host": "localhost",
    "port": 5444,
    "user": "newdbadmin",
    "password": "vertica",
    "database": "docker",
    "autocommit": True,
}

truncate_table_query = "TRUNCATE TABLE user_activity_analytics"

with vertica_python.connect(**conn_info) as connection:
    cursor = connection.cursor()
    cursor.execute(truncate_table_query)
    print("Table 'user_activity_analytics' truncated successfully.")
