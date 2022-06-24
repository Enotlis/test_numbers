Тестовое задание numbers
===========
Создание docker-контейнера
-----------
1. Клонировать репозиторий: `git clone <путь_для_клонирования>`
2. Из корня склонированного репозитория, собрать docker-контейнер для БД PostgreSQL: `sudo docker-compose build`
3. Из корня склонированного репозитория перейти в numbers_prog, собрать docker-контейнер для Google Sheets: `sudo docker build -t numbers .`
***
Quickstart для Docker
-----------
```bash
1. git clone git@github.com:Enotlis/test_numbers.git
2. cd test_numbers/
3. sudo docker-compose up -d
4. sudo docker-compose start
5. cd numbers_prog/
5. sudo docker build -t numbers .
6. sudo docker run -d --network=host numbers
7. cd ../numbers_bot/
8. sudo pip3 install -r requirements.txt
9. sudo BOT_TOKEN='ваш токен бота' python3 numbers_bot.py
```
***
Инструкция по работе с ботом
-----------
После запуск бота делаем следующее:
Отправляем команду /start и бот будет присылать уведомления
Для того чтобы завершить работу бота отправте /stop
***
Ссылка на GoogleSheets: https://docs.google.com/spreadsheets/d/1vhzenzhDNAkQCeOmqjDDfFazrTNIwdZljgQzG_xZvQw/edit?usp=drivesdk
