# AI Feed Private API Contract

Ниже контракт, который должен предоставить основной `ai-feed`.

## Аутентификация

Заголовок:

```text
X-AI-Feed-Api-Key: <secret>
```

## `POST /api/integrations/mcp/search`

Ищет релевантные источники.

### Request

```json
{
  "query": "openai agents sdk telegram",
  "limit": 8,
  "source_types": ["channel_post", "discovery_post"],
  "include_snippets": true
}
```

### Response

```json
{
  "query": "openai agents sdk telegram",
  "results": [
    {
      "id": "channel_post:123",
      "title": "@ai_news",
      "url": "https://t.me/ai_news/42",
      "snippet": "Короткий фрагмент поста...",
      "published_at": "2026-03-06T10:15:00Z",
      "source_type": "channel_post",
      "channel_username": "ai_news",
      "score": 0.91,
      "trust": {
        "opt_in": true,
        "verified_channel": false
      }
    }
  ]
}
```

## `GET /api/integrations/mcp/fetch/{source_id}`

Возвращает полный документ по идентификатору.

### Response

```json
{
  "document": {
    "id": "channel_post:123",
    "title": "@ai_news",
    "url": "https://t.me/ai_news/42",
    "content": "Полный текст поста или нормализованный контент...",
    "snippet": "Короткий фрагмент поста...",
    "published_at": "2026-03-06T10:15:00Z",
    "source_type": "channel_post",
    "channel_username": "ai_news",
    "metadata": {
      "opt_in": true,
      "verified_channel": false,
      "language": "ru"
    }
  }
}
```

## Ограничения

- Только read-only.
- Только allowlisted / `opt-in` источники.
- Возврат канонических `t.me` ссылок.
- Короткие excerpts по умолчанию.
- Без массовой выгрузки корпуса через list-all endpoints.
- В базовом варианте `ai-feed` фильтрует источники по `channels.mcp_enabled = true`.
