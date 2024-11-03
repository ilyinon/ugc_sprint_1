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
https://www.plantuml.com/plantuml/png/VPF1Zjem48RlVefvW7BfCOTgQJOiA-XkHK9FAqNJP08kYOri1zG-VST958U0ze0WC_yN-_zdUB8EZMkRMjYJL6Sqs42XcxDMf5pg_jO4tFmgi73QG5nBBWinAc2vpzPvckn-lSR9f1o_lsN9M_QWit-99q_FVr0TzAIGPDjyirnjbdcyVOqtw_TzcipQFr_o91MYH8U_qH8aDLed2qjeYcCeisnwkPl6x7gXjwDIsXYB8yrgcJwHcjLM7DP4jy7gXE6HiofEQzrQ4aBqmS72oCFHBRxTn1R1idL7RUG_T58h-51TWVMoaaLN6_bINnNZi_j7y4DV95cFnbevbev4JPK_a6EFOAkn1BwGWGCfCkYeX6BGJsy4Y_RCJ30UGUgqmGE1hlmXKbsmbYKutxGpTl0u7q3_3khEjr_0w9gi24PcS1X41Fvhu62OCjiPhNMvHv1SEh_G-2Y0FrSgyygFoAi7Is5kGsRWP4ETYarzg7xqebzBw4tSXutAHx6ITSF4aD-zaF6mhv7_2PNH0O7dx-0qy2wFAaPkr_bJx3wzUtn71SaBWL_BxZqTs4NcvG__RzD3UwNJ4A_50wqtETdqGC8K54-aohQf_mC0
