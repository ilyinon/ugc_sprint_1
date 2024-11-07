infra:
	docker-compose -f docker-compose.yml up -d --build

ugc: ugc_dir
	$(MAKE) infra
	docker-compose -f docker-compose.yml \
	-f ugc/docker-compose.yml -f ugc/docker-compose.override.yml \
	up -d --build
	docker logs -f ugc_sprint_1-ugc-1

ugc_dir:
	@:

etl: etl_dir
	$(MAKE) infra
	docker-compose -f docker-compose.yml \
	-f etl/docker-compose.yml \
	up -d --build
	docker logs -f ugc_sprint_1-etl-1

etl_dir:
	@:

kafka: kafka_dir
	docker-compose -f docker-compose.yml \
	-f kafka/docker-compose.yml up -d --build

kafka_dir:
	@:

clickhouse: clickhouse_dir
	docker-compose -f docker-compose.yml -f clickhouse/docker-compose.yml up -d --build

clickhouse_dir:
	@:

vertica: vertica_dir
	docker-compose -f docker-compose.yml -f vertica/docker-compose.yml up -d --build

vertica_dir:

all:
	$(MAKE) infra
	$(MAKE) kafka
	$(MAKE) clickhouse
	$(MAKE) ugc
	$(MAKE) etl

stop:
	docker-compose -f docker-compose.yml \
	-f ugc/docker-compose.yml \
	-f etl/docker-compose.yml \
	-f kafka/docker-compose.yml \
	-f clickhouse/docker-compose.yml down

status:
	docker-compose ps

lint:
	pre-commit install
