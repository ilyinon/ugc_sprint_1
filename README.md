##### Разработчику необходимо установить pre-commit
```bash
pre-commit install
```

#### Infrastructure

##### скопировать конфиг
```bash
cp .env_example .env
```

##### запустить nginx
```bash
make infra
```

##### запустить Kafka
```bash
make kafka
```

##### запустить Clickhouse

```bash
make infra
```

#### UGC

##### Запустить UGC
```bash
make ugc
```

##### сгенерировать тестовый access_token
```bash
docker exec  ugc_sprint_1-ugc-1 python cli/generate_access_token.py
```

##### UGC OpenAPI
```bash
http://localhost:8010/api/v1/ugc/openapi
```


#### ETL

##### Запустить ETL
```bash
make etl
```
