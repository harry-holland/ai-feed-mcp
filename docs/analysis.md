# Анализ текущего ai-feed

## Что уже можно переиспользовать

- В `bot/src/services/ai_search_service.py` уже есть retrieval по `channel_posts` и `discovery_posts`.
- В `parser/src/main.py` и `parser/src/discovery_worker.py` уже формируются канонические ссылки `https://t.me/<channel>/<message_id>`.
- В `db/src/repositories/channel_post.py` и `db/src/repositories/discovery_post.py` уже есть базовый текстовый поиск по термам.

## Главный разрыв относительно MCP-коннектора

Сейчас в проекте нет отдельного приватного API для внешнего retrieval-сценария. Есть только:

- Telegram bot;
- внутренний FastAPI для платежей.

Значит коннектору пока некуда ходить по API, хотя данные и часть retrieval-логики уже существуют.

## Архитектурный вывод

Оптимальная схема:

1. `ai-feed` становится источником данных и private retrieval API.
2. `ai-feed-mcp` становится публичным MCP gateway.
3. ChatGPT вызывает только `ai-feed-mcp`.
4. `ai-feed-mcp` не знает о БД `ai-feed` и не лезет в неё напрямую.

## Что в текущем ai-feed не подходит для публичного MVP без доработки

- ingestion через userbot/`pyrogram`;
- отсутствие выделенного allowlist/consent-флага для источников MCP;
- отсутствие нормализованного API-контракта `search` / `fetch`;
- отсутствие отдельной сервисной границы для retrieval вне Telegram-бота.

## Рекомендуемые доработки в ai-feed

- вынести общий retrieval в отдельный сервис;
- поднять приватные endpoints под API key;
- добавить явный флаг публикации источника в MCP;
- ограничить выдачу только `opt-in` источниками;
- логировать запросы коннектора отдельно от Telegram-бота.

