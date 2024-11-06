


##### отправить сгенерированные данные в UGC

Для начала, получив токен, для удобства можно сделать его экспорт в переменную, например
```bash
export TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTYxZDdkMzQtY2MyMC00ODgwLWIzODgtNDhhNDE1ZmEyNmQwIiwiZW1haWwiOiJ1c2VyQG1hLmlsIiwicm9sZXMiOiJ1c2VyIiwiZXhwIjoxNzMzNTA3OTYwLCJqdGkiOiI0MTBmOTc4NC04NDA1LTRkOTUtOGExMi04YWYyNjNjMzlkOWIifQ.3cPjeXkQQGAOpQsMNi7a877j1wyFY7yqIaX8158gGC0
```

Далее, запустить команду, где amount это количество записей для отправки:
```bash
time python3 main.py -token $TOKEN -amount 1000
```
