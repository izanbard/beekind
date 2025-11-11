from logging import getLogger

from .config import Config

config = None
app_logger = None


def get_config():
    global config
    if config is None:
        app_logger.info("Creating Config...")
        config = Config()
    return config


def get_logger():
    global app_logger
    if app_logger is None:
        app_logger = getLogger(__name__)
        app_logger.info("Creating logger...")
    return app_logger
