"""
Configure logger messages. 

References
https://docs.python.org/3/howto/logging.html
https://docs.python.org/3/library/logging.html

"""
import logging


def turn_on_logging(level="WARNING", template=None, timestamp=False):
    """Configure logger messages. 

    References
    https://docs.python.org/3/howto/logging.html
    https://docs.python.org/3/library/logging.html
    """
    if template is None:
        log_template = '%(levelname)s: %(name)s.%(message)s'
    else:
        log_template = template
    if timestamp:
        log_template += ' «%(asctime)s»'
    logger = logging.getLogger()
    _lvl = getattr(logging, level)
    logger.setLevel(_lvl)  # logging.DEBUG  logging.WARNING
    lh = logging.StreamHandler()
    formatter = logging.Formatter(log_template)
    lh.setFormatter(formatter)
    logger.addHandler(lh)
    return logger


# log_messages = True    # logger messages, turn on (log_messages=True) or off (False)
# log_timestamp = True  # add a timestamp to logger messages

# if log_messages:
#     logger = logging.getLogger()
#     logger.setLevel(logging.WARNING)  # logging.DEBUG  logging.WARNING
#     lh = logging.StreamHandler()
#     # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     log_template = '%(levelname)s: %(name)s.%(message)s'
#     if log_timestamp: log_template += ' «%(asctime)s»'
#     formatter = logging.Formatter(log_template)
#     lh.setFormatter(formatter)
#     logger.addHandler(lh)