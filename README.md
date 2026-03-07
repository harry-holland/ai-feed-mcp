# AI Feed MCP Connector

Отдельный репозиторий для MCP-коннектора, который подключается к `ai-feed` по приватному API и отдаёт ChatGPT релевантные Telegram-источники.

## Что есть сейчас

- Каркас MCP-сервера под `search` / `fetch`.
- Контракт приватного API к `ai-feed`.
- Архитектурные ограничения для безопасного MVP.

## Почему отдельный репозиторий

Заказчику нужно показывать коннектор как отдельный интеграционный продукт. При этом retrieval, индексация и ранжирование остаются в `ai-feed`, а MCP-слой занимается только:

- аутентификацией ChatGPT к коннектору;
- экспозом read-only tools;
- проксированием запросов в `ai-feed`;
- нормализацией ответа под MCP tool result.

## Рекомендуемый MVP

1. `ai-feed` даёт приватный read-only API для поиска и получения документа.
2. MCP-коннектор вызывает только этот API.
3. В индексе участвуют только `opt-in` Telegram-источники.
4. В ChatGPT возвращаются канонические `t.me` ссылки, короткий excerpt, timestamp и score.

## Почему нельзя просто использовать текущий ingest как есть

Текущий `ai-feed` уже умеет:

- собирать Telegram-посты в БД;
- хранить ссылки на `t.me/.../<message_id>`;
- делать базовый retrieval для AI Search.

Но ingestion сейчас завязан на userbot/`pyrogram` и чтение истории каналов. Для MCP-сценария это плохая точка опоры для внешней интеграции: безопаснее и презентабельнее строить коннектор поверх официального `opt-in` потока каналов, а не поверх userbot-механики.

## Инструменты MCP

### `search`

Ищет релевантные источники по запросу и возвращает список карточек:

- `id`
- `title`
- `url`
- `snippet`
- `published_at`
- `source_type`
- `channel_username`
- `score`
- `trust`

### `fetch`

Возвращает детальную карточку конкретного источника:

- `id`
- `title`
- `url`
- `content`
- `snippet`
- `published_at`
- `source_type`
- `channel_username`
- `metadata`

## Контракт с AI Feed

См. [docs/ai-feed-api-contract.md](docs/ai-feed-api-contract.md).

## Локальный запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn ai_feed_mcp.http_app:app --host 0.0.0.0 --port 8081
```

## Запуск через Docker Compose

Из корня основного проекта:

```bash
docker compose up -d --build bot ai-feed-mcp
```

После этого:

- `ai-feed` private API доступен на `http://localhost:${PAYMENT_API_PORT:-9000}`
- MCP server доступен на `http://localhost:8081`

## Переменные окружения

См. [.env.example](.env.example).

## Следующий шаг

Следующий практический шаг в основном `ai-feed`:

- вынести retrieval-логику из `AISearchWorker` в переиспользуемый сервис;
- поднять приватные endpoints `search` и `fetch`;
- добавить фильтр по `opt-in`/allowlist источникам.
