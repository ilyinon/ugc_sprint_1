infra:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d --build

auth: auth_dir
	$(MAKE) infra
	docker-compose -f docker-compose.yml -f docker-compose.override.yml \
	-f auth/app/docker-compose.yml -f auth/app/docker-compose.override.yml \
	up -d --build
	docker logs -f ugc_sprint_1-auth-1

auth_dir:
	@:

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

test_auth:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f auth/tests/functional/docker-compose.yml stop db_test_auth redis_test_auth
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f auth/tests/functional/docker-compose.yml rm db_test_auth redis_test_auth -f
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f auth/tests/functional/docker-compose.yml up db_test_auth redis_test_auth -d
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f auth/tests/functional/docker-compose.yml stop test_auth
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f auth/tests/functional/docker-compose.yml rm --force test_auth
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f auth/tests/functional/docker-compose.yml up --build -d
	docker logs ugc_sprint_1-test_auth-1 -f



all:
	$(MAKE) infra
	$(MAKE) auth
	$(MAKE) ugc
	$(MAKE) admin


remove:
	docker-compose -f docker-compose.yml stop db
	docker-compose -f docker-compose.yml rm db -f
	docker volume rm ugc_sprint_1_pg_data
stop:
	docker-compose -f docker-compose.yml -f auth/app/docker-compose.yml \
	-f ugc/app/docker-compose.yml down

status:
	docker-compose ps
