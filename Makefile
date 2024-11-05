infra:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d --build

ugc: ugc_dir
	$(MAKE) infra
	docker-compose -f docker-compose.yml -f docker-compose.override.yml \
	-f ugc/app/docker-compose.yml -f ugc/app/docker-compose.override.yml \
	up -d --build
	docker logs -f ugc_sprint_1-ugc-1

ugc_dir:
	@:

kafka: kafka_dir
	docker-compose -f docker-compose.yml -f docker-compose.override.yml \
	-f kafka/docker-compose.yml up -d --build

kafka_dir:
	@:

clickhouse: clickhouse_dir
	docker-compose -f docker-compose.yml -f clickhouse/docker-compose.yml up -d --build

clickhouse_dir:
	@:

vertica:
	docker run -d -p 5433:5433 jbfavre/vertica:latest


all:
	$(MAKE) infra
	$(MAKE) ugc
	$(MAKE) admin


remove:
	docker-compose -f docker-compose.yml stop db
	docker-compose -f docker-compose.yml rm db -f
	docker volume rm ugc_sprint_1_pg_data
stop:
	docker-compose -f docker-compose.yml \
	-f ugc/app/docker-compose.yml down

status:
	docker-compose ps
