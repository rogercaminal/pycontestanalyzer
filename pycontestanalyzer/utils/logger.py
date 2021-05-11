import logging

loggers = {}


def get_logger(name: str) -> logging:
    """Function that return the logger object
    Args:
        name (str): Name of the logger
    Returns:
        logging: Logging object returned
    """
    global loggers

    if loggers.get(name):
        return loggers.get(name)
    else:
        format_str = "[%(levelname)s: %(filename)s: %(funcName)s] %(message)s"
        logger = logging.getLogger(name)
        if logger.hasHandlers():
            logger.handlers.clear()
        logger.setLevel(logging.INFO)
        logger.propagate = False
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter(format_str)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        loggers[name] = logger

        return logger