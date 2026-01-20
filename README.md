Crypto Price Collector (Deribit)

Тестовое задание на позицию junior backend разработчика.

Сервис предназначен для периодического получения index price криптовалют BTC/USD и ETH/USD с биржи Deribit, сохранения данных в PostgreSQL и предоставления HTTP API для их получения.

Описание задачи

Приложение выполняет следующие функции:

Каждую минуту получает текущую цену (index price) для btc_usd и eth_usd

Сохраняет данные в PostgreSQL:

тикер валюты

цену

время в формате UNIX timestamp

Предоставляет HTTP API на FastAPI для работы с сохранёнными данными

Функциональность API

API реализует следующие методы (все методы используют GET):

Получение всех сохранённых данных по валюте

Получение последней цены валюты

Получение цены валюты за указанный период времени

Во всех методах обязательным является query-параметр ticker.

Используемые технологии

Python 3.12

FastAPI

PostgreSQL

SQLAlchemy (async и sync)

Celery

Celery Beat

Redis

aiohttp

Docker

Docker Compose

Alembic

Pytest

Архитектура проекта

Проект построен с разделением ответственности между слоями:

app/
├── api/            # HTTP API (роутеры, схемы)
├── core/           # Конфигурация приложения
├── db/             # Работа с БД (engine, session, models)
├── repositories/   # Слой доступа к данным
├── services/       # Бизнес-логика
├── tasks.py        # Celery-задачи
├── celery_app.py   # Конфигурация Celery
└── main.py         # Точка входа FastAPI

Переменные окружения

Настройки приложения задаются через .env файл либо значения по умолчанию:

POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_DB=prices
POSTGRES_HOST=db
POSTGRES_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379

Запуск проекта
1. Клонирование репозитория
git clone <repository_url>
cd project

2. Запуск через Docker Compose
docker compose up --build


После запуска будут подняты следующие сервисы:

FastAPI приложение (http://localhost:8000)

PostgreSQL

Redis

Celery worker

Celery Beat

Документация API

Swagger-документация доступна по адресу:

http://localhost:8000/docs

Примеры запросов
Получение последней цены валюты
GET /prices/latest?ticker=btc_usd

Получение всех цен валюты
GET /prices/all?ticker=eth_usd

Получение цен за период времени
GET /prices/range?ticker=btc_usd&from_ts=1705708800&to_ts=1705712400


Параметры from_ts и to_ts передаются в формате UNIX timestamp (секунды).

Работа с базой данных
Применение миграций
docker compose exec app alembic upgrade head

Проверка сохранённых данных
docker compose exec db psql -U user -d prices

SELECT * FROM prices ORDER BY timestamp DESC;

Тестирование

Для основных сервисных методов реализованы unit-тесты с использованием моков.

Запуск тестов
pytest

Design decisions
Использование Celery для периодических задач

Celery используется для фонового сбора данных, Celery Beat отвечает за расписание выполнения задач с периодичностью в одну минуту.

Разделение sync и async доступа к БД

Асинхронный SQLAlchemy используется в HTTP API

Синхронный SQLAlchemy используется в Celery-задачах

Такой подход упрощает выполнение фоновых задач и снижает риск ошибок при работе с event loop.

Использование UNIX timestamp

В проекте используется единый формат времени — UNIX timestamp, что упрощает хранение, фильтрацию и обработку данных.

Repository и Service слои

Репозитории отвечают за доступ к данным

Сервисы содержат бизнес-логику

Это улучшает читаемость кода и упрощает unit-тестирование.

Клиент Deribit

Для работы с API Deribit используется aiohttp, что позволяет выполнять асинхронные HTTP-запросы с минимальными накладными расходами.

Соответствие требованиям ТЗ

Клиент Deribit реализован

Периодический сбор данных реализован через Celery

PostgreSQL используется в качестве базы данных

HTTP API реализовано на FastAPI

Все методы используют GET и принимают параметр ticker

Unit-тесты реализованы для основных методов

Проект разворачивается через Docker Compose