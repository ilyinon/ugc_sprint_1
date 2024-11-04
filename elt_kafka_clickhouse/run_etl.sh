echo "Запуск run_etl.sh script..."
set -e

while ! nc -z $ELASTIC_HOST $ELASTIC_PORT; do
      echo "No connect elastic..." $ELASTIC_HOST $ELASTIC_PORT

      sleep 10
done


while ! nc -z $ELASTIC_HOST $ELASTIC_PORT; do
      echo "No connect elastic..." $ELASTIC_HOST $ELASTIC_PORT

      sleep 10
done