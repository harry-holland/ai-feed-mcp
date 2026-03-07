import httpx

from .config import Settings
from .models import FetchResponse, SearchInput, SearchResponse


class AIFeedClient:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._headers = {
            "X-AI-Feed-Api-Key": settings.ai_feed_api_key,
        }

    async def search(self, payload: SearchInput) -> SearchResponse:
        async with httpx.AsyncClient(
            base_url=self._settings.ai_feed_api_base_url.rstrip("/"),
            timeout=self._settings.ai_feed_timeout_seconds,
            headers=self._headers,
        ) as client:
            response = await client.post(
                "/api/integrations/mcp/search",
                json=payload.model_dump(mode="json"),
            )
            response.raise_for_status()
            return SearchResponse.model_validate(response.json())

    async def fetch(self, source_id: str) -> FetchResponse:
        async with httpx.AsyncClient(
            base_url=self._settings.ai_feed_api_base_url.rstrip("/"),
            timeout=self._settings.ai_feed_timeout_seconds,
            headers=self._headers,
        ) as client:
            response = await client.get(
                f"/api/integrations/mcp/fetch/{source_id}",
            )
            response.raise_for_status()
            return FetchResponse.model_validate(response.json())

