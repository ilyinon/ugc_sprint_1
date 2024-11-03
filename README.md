# Проектная работа 8 спринта


##### скопировать конфиг
```bash
cp .env_example .env
```

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


##### Установить pre-commit
```bash
pre-commit install
```
