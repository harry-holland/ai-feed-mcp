import contextlib

from starlette.applications import Starlette
from starlette.routing import Mount

from .config import Settings
from .server import create_mcp_server

settings = Settings()
mcp = create_mcp_server(settings)


@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with mcp.session_manager.run():
        yield


app = Starlette(
    routes=[
        Mount("/", app=mcp.streamable_http_app()),
    ],
    lifespan=lifespan,
)
