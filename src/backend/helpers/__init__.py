from logging import getLogger, Logger

# from local files
from .config import Config

config = None
app_logger = None


def get_config() -> Config:
    global config
    logger = get_logger()
    if config is None:
        logger.info("Creating Config...")
        config = Config()
    return config


def get_logger() -> Logger:
    global app_logger
    if app_logger is None:
        app_logger = getLogger(__name__)
        app_logger.info("Creating logger...")
    return app_logger
