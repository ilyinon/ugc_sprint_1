echo "Запуск run_etl.sh script..."
set -e

while ! nc -z $CLICKHOUSE_HOST $CLICKHOUSE_PORT; do
      echo "No connect elastic..." $CLICKHOUSE_HOST $CLICKHOUSE_PORT

      sleep 10
done


echo "Etl запущен."
python main.py