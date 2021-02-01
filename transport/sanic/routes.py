from transport.sanic.endpoints.health import HealthEndpoint
from configs.config import ApplicationConfig

def get_routes(config: ApplicationConfig):
    return (
        HealthEndpoint(config, '/', methods=['GET', 'POST']),
    )