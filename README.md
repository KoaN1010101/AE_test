# PROJECT MANAGER 

## Веб-приложение «Проектный менеджер», включающий следующий функционал: 
- Регистрация, авторизация. Два уровня: администратор, пользователь.
-	Иерархическая структура проектов и подпроектов. Админ может создавать, редактировать, удалять. Любой пользователь может получить структуру.
- Задачи для любого уровня проекта\подпроекта. Задачи делятся на два типа: для менеджера, для технического специалиста. Должны содержать название, статус (new, progress, done), дату создания, дату изменения статуса, стандартную информацию для конкретного типа.
-	Любой пользователь может создать задачу для любого уровня проекта\подпроекта, изменить статус, удалить свою задачу, посмотреть все задачи. Любой администратор может редактировать, удалить задачу.

# Установка
## Склонируйте репозиторий:
```
git clone git@github.com:KoaN1010101/Project_manager.git
```
## Активируйте venv и установите зависимости:
```
python3 -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```
## Создайте в корневой директории файл .env со следующим наполнением:
```
APP_TITLE=<ваше название приложения>
DATABASE_URL=<настройки подключения к БД, например: sqlite+aiosqlite:///./development.db>
SECRET=<секретный ключ>
```
# Управление:

## Выполнить миграции
```
alembic upgrade head
```
## Запустить приложение
```
uvicorn app.main:app --reload
```
