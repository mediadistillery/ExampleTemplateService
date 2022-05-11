import logging
import sys


def set_logging(filepath=None, stream=None, level=logging.INFO, multithreaded=False, multiprocessed=False):
    """Only top level scripts should call this function."""
    log_format = '%(asctime)s - '
    if multiprocessed:
        log_format += '%(process)d - '
    log_format += '%(levelname)-8s - '
    if multithreaded:
        log_format += '%(threadName)s - '
    log_format += '%(name)s - %(message)s'

    level = level.upper() if isinstance(level, str) else level

    if not (filepath is None or stream is None):
        raise ValueError("'filepath' and 'stream' should not be specified together")
    elif filepath is not None:
        logging.basicConfig(level=level, format=log_format, filename=filepath)
    elif stream is not None:
        logging.basicConfig(level=level, format=log_format, stream=stream)
    else:
        logging.basicConfig(level=level, format=log_format)

    sys.excepthook = _exception_hook


def _exception_hook(exc_type, exc_value, exc_traceback):
    """Simple function to ensure unexpected exceptions are still logged"""
    logging.exception('Uncaught exception', exc_info=(exc_type, exc_value, exc_traceback))
