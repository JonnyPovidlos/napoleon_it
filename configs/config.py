from transport.sanic.config import SaincConfig
from db.config import SQLiteConfig

class ApplicationConfig:
    sanic: SaincConfig
    database: SQLiteConfig

    def __init__(self):
        self.sanic = SaincConfig()
        self.database = SQLiteConfig()