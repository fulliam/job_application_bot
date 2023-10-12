# Поисковый робот для отклика на вакансии hh.ru, использующий модули `sklearn` для сравнения вашего резюме с описанием вакансий.

## Для начала работы, требуется:

### Клонировать репозиторий  
```bash
git clone https://github.com/fulliam/job_application_bot.git
```
#### Перейти в папку репозитория  
```bash
cd /job_application_bot
```
### Установить зависимости  
```bash
pip instal -r requirements.txt
```

## Создать базу данных, роль и подключить uuid   
**Вход под суперпользователем**  
```bash
sudo su postgres
```
**Запуск psql**  
```bash
psql
```
**Создать базу данных**  
```bash
CREATE DATABASE search_job;
```
**Создать роль для базы данных**  
```bash
CREATE USER admin_search_job WITH LOGIN PASSWORD 'adminpassword';
```
**Выдать все права на базу данных для роли**  
```bash
GRANT ALL PRIVILEGES ON DATABASE search_job TO admin_search_job;
```

### Создать в корневом каталоге репозитория файл .env  
**Содержимое файла:**  
```bash
DB_USER = "admin_search_job"
DB_PASS = "adminpassword"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "search_job"
```

### ⚠️ Отредактировать `bot_all.py` в соответствии со своим запросом и протестировать его работу на *НЕАВТОРИЗИРОВАННОМ* сайте (советую поиграть с настройками). Запуск:
```bash
python3 bot_all.py
```
### Когда бот настроен и открывает подходящие Вам вакансии, удалите текущую таблицу поисков:
```bash
DROP TABLE dev;
```
### Авторизируйтесь на сайте и запустите Вашего автооткликатора! Enjoy 🥳
```bash
python3 bot_all.py
```