echo "Запуск run_etl_elactic.sh script..."
set -e

while ! nc -z $ELASTIC_HOST $ELASTIC_PORT; do
      echo "No connect elastic..." $ELASTIC_HOST $ELASTIC_PORT

      sleep 10
done


echo "Запуск run_etl_elactic.sh script..."
set -e

while ! nc -z $ELASTIC_HOST $ELASTIC_PORT; do
      echo "No connect elastic..." $ELASTIC_HOST $ELASTIC_PORT

      sleep 10
done