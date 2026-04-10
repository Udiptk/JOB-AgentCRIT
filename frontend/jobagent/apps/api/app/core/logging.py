import sys
from loguru import logger


def setup_logging():
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> — <level>{message}</level>",
        level="INFO",
        colorize=True,
    )
    logger.add(
        "logs/jobagent.log",
        rotation="10 MB",
        retention="7 days",
        level="DEBUG",
    )
