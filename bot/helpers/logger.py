import logging
import os

def get_logger(name=__name__):
    logs_dir = 'logs'
    log_file = os.path.join(logs_dir, 'bot.log')

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    if not os.path.exists(log_file):
        open(log_file, 'a').close()

    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(log_file, encoding='utf8')
        formatter = logging.Formatter(
            "[%(asctime)s][%(levelname)s][%(name)s] %(message)s"
        )
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
    return logger
