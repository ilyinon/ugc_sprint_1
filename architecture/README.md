Основной точкой входа для пользователей и сотрудников является nginx( кластер балансеров), которые перенаправляют трафик на целевые сервера:
 - search
 - auth
 - adminka
 - UGC

 Используются следующие системы хранения, кеширования и поиска данных:
  - postgresql
  - redis
  - elastic
  - kafka (kraft)
  - clickhouse


Общая схема выглядит так:

![alt text](https://www.plantuml.com/plantuml/png/PP6_JWCn3CRtF8NLlPLOEw12GHqGLLN4LDtWvjmsN9gWYwy28HPcte5NG4Y80ObdkBuHzySLf3V5_kBVvzXHQXGOSowsLWtBj_Ad_Dw_bb_L-L6-xr_AppeV0lJxfx2OherxW9F1O9ee5MMB6y9SRwhWhE3cIBV6PLX5jvDnekBorks0T6_4ewkBQVUgxIAMiOj0aQXKYenB30IzcG-ypYdqu4b1Mm0NvqaTZxrZSjoap_-PIuk1ZHRaskyCXOQOKHwyQ-C9kLpakRSKZZpcb9f3Kurw8wLOzrzQr1dSiJbYhd2LeJ3ixuqEiF8vq8uSLtXSFBP6PnjV13eGkBGKW3sWG_iOg2NY5SLJnnkLiO_bPXBvUf5aYoB6TVLVYTBC4ob_ZqxKY5nQREql)
