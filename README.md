# 11_03_2024_test
Это выполненое задание:
Находится в каталоге data


## Все просто:
- Выполнено на Python 3.11
- Используем браузер Chrome
- Подготовка:
  - Клонируем
  - Создаем виртуальную среду `py -3.11 -m venv venv` 
  - Пользовватели Windows включают `venv\scripts\activate` 
  - Установить из requirements.txt зависимости `pip install -r requirements.txt` 
  - Необходимо создать `.env` файл в `11_03_2024_test` и в нем указать:
    ```
    proxy_ip= прокси api
    proxy_login= прокси логин
    proxy_password= прокси пароль
    ```
  - Загрузить сертификат командой `python -m seleniumwire extractcert` и установить
   - Или используя ссылку: https://github.com/wkeeling/selenium-wire/raw/master/seleniumwire/ca.crt
  - Загрузить драйвер Chrome в каталог data по ссылке: https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.128/win64/chromedriver-win64.zip
   - Эндпойнты всех загрузок: https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json
- Запуск:
  - Входим командой к файлу phomebook.py: `python main.py` 
  - Автоматическая работа на сайте специально слелана медленной дабы имитировать работу пользователя.
- Результат:
  - csv файл с результатом(пример `1710792547654796900_data.csv`).
  - Последние 10 твитов Маска в терминале.

 

#### Буду рад критике
