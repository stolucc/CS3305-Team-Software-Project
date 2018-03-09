"""Logging handler that logs to a file."""
import logging


class Logger:
    """Logger class that sets up the logging."""

    def __init__(self, log_file, logger_name, log_level):
        """
        Create a Logger object.

        :param log_file: path of the log file
        :param logger_name: name of the logger
        :param log_level: minimum log level to be recorded
        """
        log_level = getattr(logging, log_level, None)
        log_format = '[%(asctime)s] %(levelno)s, %(levelname)s ' \
                     '[%(filename)s, %(lineno)d, %(funcName)s ' \
                     '%(name)s, %(process)d, %(processName)s, ' \
                     '%(thread)d, %(threadName)s] %(message)s'
        logging.basicConfig(filename=log_file, level=log_level,
                            format=log_format)
        logging.raiseExceptions = False
        self.log = logging.getLogger(logger_name)

    def get_logger(self):
        """Return a log object."""
        return self.log
