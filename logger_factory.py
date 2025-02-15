import logging.config
import logging.handlers
import yaml
from logging import getLogger
import logging
# import coloredlogs


class LoggerFactory:
    def getLogger(logger_name):
        logging.config.dictConfig(
            yaml.safe_load(open("log_config.yaml").read()))

        logger = getLogger(f"app.{logger_name}")
        # coloredlogs.install(logger=logger,level=logger.level)

        return logger
