import logging
import os
import pathlib
from typing import Union

from dotenv import load_dotenv


def _create_logger(log_level: Union[str, None] = None):
    if log_level is None:
        log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_level_int = getattr(logging, log_level)
    ch = logging.StreamHandler()
    ch.setLevel(log_level_int)
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    ch.setFormatter(formatter)
    _logger = logging.getLogger(__name__)
    _logger.addHandler(ch)
    _logger.setLevel(log_level_int)
    return _logger


logger = _create_logger()

# LOAD .env file path from ENV_PATH environment variable
env_path = os.getenv("ENV_PATH", ".env")
if pathlib.Path(env_path).is_file():
    logger.info("Loading .env from %s", env_path)
    load_dotenv(env_path, override=False)
else:
    logger.info("Skipping optional loading of .env file.")


from .app import create_app  # noqa: E402

app = create_app(os.getenv("FLASK_CONFIG") or "default")
