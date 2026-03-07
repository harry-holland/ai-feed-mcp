import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from .client import AIFeedClient
from .config import Settings
from .models import SearchInput


def _search_result_to_content(query: str, data: dict[str, Any]) -> str:
    return json.dumps(
        {
            "query": query,
            "results": data.get("results", []),
        },
        ensure_ascii=False,
        indent=2,
        default=str,
    )


def _fetch_result_to_content(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, default=str)


def create_mcp_server(settings: Settings | None = None) -> FastMCP:
    settings = settings or Settings()
    client = AIFeedClient(settings)
    mcp = FastMCP(
        name=settings.mcp_server_name,
        version=settings.mcp_server_version,
        stateless_http=True,
        json_response=True,
    )

    @mcp.tool(
        name="search",
        description=(
            "Search relevant Telegram sources from AI Feed and return canonical "
            "t.me links with snippets, timestamps and trust signals."
        ),
    )
    async def search_tool(
        query: str,
        limit: int = 8,
    ) -> str:
        payload = SearchInput(query=query, limit=limit)
        result = await client.search(payload)
        return _search_result_to_content(query, result.model_dump(mode="json"))

    @mcp.tool(
        name="fetch",
        description=(
            "Fetch the full normalized document for a previously returned AI Feed source id."
        ),
    )
    async def fetch_tool(source_id: str) -> str:
        result = await client.fetch(source_id)
        return _fetch_result_to_content(result.model_dump(mode="json"))

    @mcp.tool(
        name="search_sources",
        description=(
            "Convenience alias for search when the client only needs linkable source cards."
        ),
    )
    async def search_sources_tool(
        query: str,
        limit: int = 8,
    ) -> str:
        payload = SearchInput(query=query, limit=limit)
        result = await client.search(payload)
        return _search_result_to_content(query, result.model_dump(mode="json"))

    return mcp
