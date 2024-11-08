#### Ссылка на репозиторий
```bash
https://github.com/ilyinon/ugc_sprint_1
```


##### Документация
Документация находится в каталоге docs

[docs/architecture/architecture.md](docs/architecture/architecture.md) - текущая high-level архитектура и проекта UGC

[docs/requirements/functional.md](docs/requirements/functional.md) - функциональные требования

[docs/requirements/non-functinal.md](docs/requirements/non-functinal.md) - нефункциональные требования

[docs/research/report.md](docs/research/report.md) - результат исследования




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

#### Доступ gj UI


##### Kafka UI
```bash
http://localhost:8080/
```

##### Clickhouse UI
```bash
http://localhost:5521/
```



#### Ислледование и сравнение Vertica с Clickhouse

Все скрипты для запуска находятся в каталоге
[ugc/app/data](ugc/app/data) - результат исследования



Из предыдущих шагов должен быть запущен инстанс Clickhouse, или запустить
```bash
make clickhouse
```


для запуска Vertica выполнить команду:
```bash
make vertica
```


Запустить генератор данных Vertica
##### выполнить следующие команды
```bash
cd ugc/app/data/ && \
python vertica_table.py
clickhouse_table.py vertica_data_generator.py
```


```bash
vertica_transactions.py
````


Запустить генератор данных Clickhouse
##### выполнить следующие команды
```bash
cd ugc/app/data/ && \
python clickhouse_table.py
clickhouse_table.py clickhouse_data_generator.py
```

```bash
clickhouse_transactions.py
````
