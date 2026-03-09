# Public Access Model

This document describes how to make the connector publicly usable without exposing privileged access to the main `ai-feed` system.

## Goal

Any user should be able to run the connector or connect it in ChatGPT, but nobody should receive broad internal access to `ai-feed`.

## What Must Stay Private

- database access
- parser control
- channel management
- admin endpoints
- write operations
- bulk export access
- shared master API keys

The connector should never contain those permissions.

## Recommended Model

Use personal read-only integration tokens issued by `ai-feed`.

Flow:

1. A user creates an account in `ai-feed`.
2. The user generates an MCP token via the bot command `/mcp_token`.
3. The token is shown once and then stored hashed server-side.
4. The user places that token into the connector environment.
5. The connector uses the token only for MCP read endpoints.

## Token Properties

Each token should have:

- owner user id
- token id
- hashed secret
- status: active / revoked
- creation time
- optional expiry time
- scope list
- rate-limit profile

## Minimal Scope Set

For this connector the scope should be as narrow as possible:

- `mcp.search`
- `mcp.fetch`

Nothing else.

Not allowed:

- channel create/update/delete
- parser task management
- user management
- billing actions
- discovery/admin mutations

## Access Control Modes

There are two sane modes.

### 1. Global Editorial Feed

All users search the same allowlisted MCP corpus.

Use when:

- the product is a public research feed
- the same source set is acceptable for everyone

Backend policy:

- search only over `mcp_enabled` sources
- token identifies user only for quota and abuse control

### 2. Personal Feed

Each user searches only data they are entitled to access.

Use when:

- `ai-feed` is a personal workspace product
- users should only see their own subscriptions or purchased datasets

Backend policy:

- token resolves to user
- backend applies per-user filtering before search/fetch

## Recommended First Production Version

Start with:

- public connector repository
- private `ai-feed` backend
- personal read-only tokens
- global allowlisted corpus
- per-token rate limits

This gives a simple and safe rollout without exposing internal capabilities.

## Why Not A Shared Global Secret

A shared backend key is acceptable only for internal demos.

Problems with a shared secret:

- impossible to revoke one bad actor cleanly
- impossible to attribute abuse
- impossible to apply per-user quotas
- once leaked, every deployment is compromised

## Better Than A Shared Secret

From best to acceptable:

1. OAuth with user-bound access tokens
2. Personal long-lived integration tokens with narrow scopes
3. Short-lived signed tokens minted by `ai-feed`

For MVP, option 2 is the best tradeoff.

## Connector-Side Rules

The connector should remain dumb and low-privilege:

- proxy only `search` and `fetch`
- pass the user token to `ai-feed`
- do not store long-term secrets except the configured read-only token
- do not embed admin credentials
- do not add mutation tools

## Backend Rules

The main `ai-feed` service should enforce:

- token validation
- scope checks
- source allowlisting
- rate limits
- request logging
- revocation
- optional expiry

The backend, not the connector, should be the final policy gate.

## Suggested Next Backend Step

Add an integrations table in `ai-feed` for MCP tokens with:

- `id`
- `user_id`
- `name`
- `token_hash`
- `scopes`
- `is_active`
- `last_used_at`
- `expires_at`
- `rate_limit_tier`

Then require those tokens for:

- `POST /api/integrations/mcp/search`
- `GET /api/integrations/mcp/fetch/{source_id}`

## Practical Recommendation

For the public repo:

- keep README simple
- show how to run with a personal token
- avoid any examples with admin or global secrets

For internal demo:

- a shared demo token is acceptable temporarily
- but do not present that as the production model
