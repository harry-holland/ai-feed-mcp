from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


SourceType = Literal["channel_post", "discovery_post"]


class TrustSignals(BaseModel):
    opt_in: bool = False
    verified_channel: bool = False


class SearchInput(BaseModel):
    query: str = Field(min_length=3)
    limit: int = Field(default=8, ge=1, le=20)
    source_types: list[SourceType] = Field(
        default_factory=lambda: ["channel_post", "discovery_post"]
    )
    include_snippets: bool = True


class SearchResult(BaseModel):
    id: str
    title: str
    url: str
    snippet: str | None = None
    published_at: datetime | None = None
    source_type: SourceType
    channel_username: str | None = None
    score: float | None = None
    trust: TrustSignals = Field(default_factory=TrustSignals)


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]


class FetchResponse(BaseModel):
    document: "SourceDocument"


class SourceDocument(BaseModel):
    id: str
    title: str
    url: str
    content: str
    snippet: str | None = None
    published_at: datetime | None = None
    source_type: SourceType
    channel_username: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


FetchResponse.model_rebuild()

