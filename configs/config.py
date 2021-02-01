from transport.sanic.config import SaincConfig

class ApplicationConfig:
    sanic: SaincConfig

    def __init__(self):
        self.sanic = SaincConfig()