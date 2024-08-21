import logging
from pylogrus import PyLogrus, TextFormatter

def init_logrus():
    logging.setLoggerClass(PyLogrus)

    logger = logging.getLogger(__name__)  # type: PyLogrus
    logger.setLevel(logging.INFO)

    formatter = TextFormatter(datefmt="Z", colorize=True)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger