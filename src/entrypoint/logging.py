import inspect
import logging
import sys
import typing

from loguru import logger

if typing.TYPE_CHECKING:
    pass


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def config_logger(level: str, env: str) -> None:
    # https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    logger.remove()
    if env in ("dev", "test"):
        logger.add(sys.stderr, level=level)
    else:
        logger.add(sys.stderr, level=level, serialize=True)  # type: ignore [reportArgumentIssue, reportCallIssue]
