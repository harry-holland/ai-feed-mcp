from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ai_feed_api_base_url: str = Field(..., alias="AI_FEED_API_BASE_URL")
    ai_feed_api_key: str = Field(..., alias="AI_FEED_API_KEY")
    ai_feed_timeout_seconds: float = Field(
        20.0,
        alias="AI_FEED_TIMEOUT_SECONDS",
    )
    mcp_server_name: str = Field("ai-feed", alias="MCP_SERVER_NAME")
    mcp_server_version: str = Field("0.1.0", alias="MCP_SERVER_VERSION")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

