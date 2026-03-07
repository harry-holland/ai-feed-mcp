from .config import Settings
from .server import create_mcp_server


def main() -> None:
    settings = Settings()
    server = create_mcp_server(settings)
    server.run(transport="streamable-http")


if __name__ == "__main__":
    main()
