import sys

import logfire
from loguru import logger

STYLE_BY_LEVEL: dict[str, tuple[str, str, str]] = {
    "TRACE": ("🔍", "<white>", "</white>"),
    "DEBUG": ("🐛", "<cyan>", "</cyan>"),
    "INFO": ("🔵", "<blue>", "</blue>"),
    "SUCCESS": ("✅", "<green>", "</green>"),
    "WARNING": ("⚠️ ", "<yellow>", "</yellow>"),
    "ERROR": ("🚨", "<red>", "</red>"),
    "CRITICAL": ("💀", "<bold><red>", "</red></bold>"),
}


def colour_and_emoji_format(record: dict) -> str:
    emoji, open_tag, close_tag = STYLE_BY_LEVEL.get(record["level"].name, ("", "<white>", "</white>"))
    return (
        f"{open_tag}{emoji} {record['time']:YYYY-MM-DD HH:mm:ss} | "
        f"{record['level'].name:<8} | {record['message']}{close_tag}\n"
    )


# Remove default logging config
logger.remove()

# Terminal output (INFO and higher)
logger.add(sink=sys.stdout, format=colour_and_emoji_format, level="INFO")  # type: ignore  # noqa: PGH003

# File logging (DEBUG and higher)
logger.add(
    sink="logs/log.log",
    rotation="1 MB",
    retention=5,
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {file} | {level} | {message}",
    level="DEBUG",
)

# Add logfire sink
logfire.configure(token="{{cookiecutter.logfire_token}}", console=False, min_level="info")  # noqa: S106

logger.add(**logfire.loguru_handler())

if __name__ == "__main__":
    # Sample logs
    logger.trace("Starting potato audit.")
    logger.debug("Parsed 42 entries from JSON.")
    logger.info("Committee form loaded.")
    logger.success("Potato order submitted.")
    logger.warning("Missing quantity for red potatoes.")
    logger.error("Payment gateway timeout.")
    logger.critical("Audit trail corrupted.")
