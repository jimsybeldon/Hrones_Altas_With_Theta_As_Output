import logging
import yaml

def setup_logging():
    with open("settings.yaml", "r") as f:
        settings = yaml.safe_load(f)

    log_file = settings["logging"]["file"]
    log_level = settings["logging"]["level"]

    logging.basicConfig(
        filename=log_file,
        level=getattr(logging, log_level),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    logger = logging.getLogger(__name__)
    logger.info("Logging initialized.")
    return logger
