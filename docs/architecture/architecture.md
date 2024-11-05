#### Основной точкой входа для пользователей и сотрудников является nginx( кластер балансеров), которые перенаправляют трафик на целевые сервера:
* search
* auth
* adminka
* UGC

#### Используются следующие системы хранения, кеширования и поиска данных:
* postgresql
* redis
* elastic
* kafka (kraft)
* clickhouse


#### Общая схема выглядит так:

![alt text](https://www.plantuml.com/plantuml/png/PP6_JWCn3CRtF8NLlPLOEw12GHqGLLN4LDtWvjmsN9gWYwy28HPcte5NG4Y80ObdkBuHzySLf3V5_kBVvzXHQXGOSowsLWtBj_Ad_Dw_bb_L-L6-xr_AppeV0lJxfx2OherxW9F1O9ee5MMB6y9SRwhWhE3cIBV6PLX5jvDnekBorks0T6_4ewkBQVUgxIAMiOj0aQXKYenB30IzcG-ypYdqu4b1Mm0NvqaTZxrZSjoap_-PIuk1ZHRaskyCXOQOKHwyQ-C9kLpakRSKZZpcb9f3Kurw8wLOzrzQr1dSiJbYhd2LeJ3ixuqEiF8vq8uSLtXSFBP6PnjV13eGkBGKW3sWG_iOg2NY5SLJnnkLiO_bPXBvUf5aYoB6TVLVYTBC4ob_ZqxKY5nQREql)


#### Cхема взаимодействия UGS, ETL, Kafka, Clickhouse выглядит так:
![alt test](https://www.plantuml.com/plantuml/png/PP51JyCm38Nl_XLMpw29woJGq8Gum0qu8JIPp5L3swIAqqxxzpWk6uFwC7dnUv_yNDX8ffJ7lWDoEIQiKmnvvphF8OFMe5Fl_40XuzlZ5jy1jMvBAvmcxzWUhhMigQeL3NurtQno8jVkU59GLS77NzGJrIsTOFRdFoR7mJkyWCYIyl3wV69eko0a2bB7rEEUCitkqdsIC6uxxzecZiBma_m-K7TKj01S7a69ToNvMlE6FSwhO8xwzd8-WSvDPqdME77ojJ_Yro6hikM05FQsnPLHYdqERRzcrG1h2-HYaB5dCNtv7ZtQBGHqQjBVtSrXo5bUmAvCqGTqpHXQWNEkXRUXYP6SOx501f3OSnCF0B1HwjXttm00)
