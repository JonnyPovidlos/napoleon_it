from context import Context
from transport.sanic.endpoints.health import HealthEndpoint
from configs.config import ApplicationConfig


def get_routes(config: ApplicationConfig, context: Context):
    return (
        HealthEndpoint(config=config, context=context, uri='/', methods=['GET', 'POST'], ),
    )