# AI Feed MCP Connector

Standalone MCP connector for `ai-feed`.

It exposes read-only MCP tools for ChatGPT and proxies all retrieval to a protected `ai-feed` backend. The connector does not read Telegram directly and does not need database access.

## What It Does

- Exposes MCP tools: `search`, `search_sources`, `fetch`
- Calls the private `ai-feed` API for retrieval
- Returns canonical `t.me/...` links, snippets and metadata
- Works as a separate repository that can be shown and deployed independently

## Architecture

```text
ChatGPT -> AI Feed MCP Connector -> AI Feed Private API -> AI Feed index
```

The connector is intentionally thin:

- no direct database access
- no write operations
- no Telegram userbot logic
- no corpus export endpoints

## MCP Endpoint

The Streamable HTTP MCP endpoint is:

```text
/mcp
```

Example public URL:

```text
https://your-domain.example/mcp
```

## Available Tools

### `search`

Search relevant Telegram sources for a query.

### `search_sources`

Alias for `search` when the client only needs linkable source cards.

### `fetch`

Fetch the full normalized document for a previously returned source id.

## Requirements

- Python 3.12+
- an `ai-feed` backend with MCP private API enabled
- an `AI_FEED_API_KEY` with read-only MCP scope

## Environment Variables

See [.env.example](.env.example).

Required:

```env
AI_FEED_API_BASE_URL=http://localhost:9000
AI_FEED_API_KEY=your-read-only-token
```

Get `AI_FEED_API_KEY` from the AI Feed bot:

```text
/mcp_token
```

The bot issues a personal MCP token for the current user. Reissuing the token invalidates the previous one.

Optional:

```env
AI_FEED_TIMEOUT_SECONDS=20
MCP_SERVER_NAME=ai-feed
MCP_SERVER_VERSION=0.1.0
MCP_SERVER_PORT=8081
```

## Local Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn ai_feed_mcp.http_app:app --host 0.0.0.0 --port 8081
```

Then the MCP endpoint is:

```text
http://localhost:8081/mcp
```

## Run With Docker

```bash
docker build -t ai-feed-mcp .
docker run --rm -p 8081:8081 --env-file .env ai-feed-mcp
```

Then the MCP endpoint is:

```text
http://localhost:8081/mcp
```

## Run From The Main Project

From the main `ai-feed` repository:

```bash
docker compose up -d --build bot ai-feed-mcp
```

With the current compose mapping:

- `ai-feed` private API: `http://localhost:9000`
- MCP server: `http://localhost:8083/mcp`

## Connect In ChatGPT

1. Deploy the connector behind public HTTPS.
2. Use the public MCP URL ending with `/mcp`.
3. Add it in ChatGPT as a custom MCP connector.
4. Use read-only auth or no-auth only for internal demos.

Important:

- opening the MCP URL in a browser is not a useful health check
- the correct check is that the endpoint responds as MCP transport on `/mcp`

## Security Model

This repository can be public, but the backend access must stay restricted.

Recommended production model:

- every `ai-feed` user gets a personal integration token
- the token is scoped only for MCP read operations
- the connector never gets database credentials
- the backend enforces rate limits, revocation and per-user quotas

Current token issue flow:

- user opens the AI Feed bot
- user runs `/mcp_token`
- bot returns a personal MCP token
- user places that token into `AI_FEED_API_KEY`

See [docs/public-access-model.md](docs/public-access-model.md).

## Private API Contract

See [docs/ai-feed-api-contract.md](docs/ai-feed-api-contract.md).

## Current Status

This repository is ready for:

- local development
- standalone deployment
- ChatGPT MCP integration

What still belongs to the main `ai-feed` system:

- user account lifecycle
- token issuance
- source allowlisting
- rate limiting
- per-user access policy
