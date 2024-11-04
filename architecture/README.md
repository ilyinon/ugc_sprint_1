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

![alt text](https://www.plantuml.com/plantuml/png/VPB13X8n48RlVOe1pv1uC34S3B0G3aP2C9u8XzdkmDRjjgJjeiPuyUmx-0h6n7WmyHcMDxAKDbf8t4kdV-VxfpFRgNLeNDTADd0rjGJsX9mabcnGqK4eWjLskLp3azdpnRFvZDb6g1CQRA54tXoDxbHLQAaDlAk58yOc_TV-T__hygN_wTVl_RVBv_x7TJy168rUm6vz5EezF1sFrtl6ijtkDQ7XjGzcdGjBrGhLe8_Uh0gVpN8W-2NeyIIvFEh9zl4er4cMcKk2_YEccuIlGeSbMeBXHbjtD6I7y9713ON5V7-D2wqSAHUsd_vbbXAj4pmYh_HPa0t4XepLwXQlI9aeRxNqKUwnfKgaeXnv7LFnMh-Ko1juwyGTyn8F3KR6wPFW5WxQ09r9EO_doOKKlAbrPoaHM4gou3IWGld1qet8vvHtdSywjdqlXqxYiuXIcc8cfZp_5wCI-icKlvVUiocfoZ_zFm00)


Cхема взаимодействия UGS, ETL, Kafka, Clickhouse выглядит так:
![alt test](https://www.plantuml.com/plantuml/png/PP51JyCm38Nl_XLMpw29woJGq8Gum0qu8JIPp5L3swIAqqxxzpWk6uFwC7dnUv_yNDX8ffJ7lWDoEIQiKmnvvphF8OFMe5Fl_40XuzlZ5jy1jMvBAvmcxzWUhhMigQeL3NurtQno8jVkU59GLS77NzGJrIsTOFRdFoR7mJkyWCYIyl3wV69eko0a2bB7rEEUCitkqdsIC6uxxzecZiBma_m-K7TKj01S7a69ToNvMlE6FSwhO8xwzd8-WSvDPqdME77ojJ_Yro6hikM05FQsnPLHYdqERRzcrG1h2-HYaB5dCNtv7ZtQBGHqQjBVtSrXo5bUmAvCqGTqpHXQWNEkXRUXYP6SOx501f3OSnCF0B1HwjXttm00)
