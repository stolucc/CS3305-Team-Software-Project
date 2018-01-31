"""Logging handler that logs to the posgres database."""
import logging
import time
from database_API import Log


class Logger:
    """Logger class that sets up the logging."""

    def __init__(self, session, logger_name, log_level):
        """
        Create a Logger object.

        :param session: sessionmaker object
        :param logger_name: name of the logger
        :param log_level: minimum log level to be recorded
        """
        logging_handler = LoggingHandler(session)
        logging.getLogger('').addHandler(logging_handler)
        self.log = logging.getLogger(logger_name)
        self.log.setLevel(log_level)

    def get_logger(self):
        """Return a log object."""
        return self.log


class LoggingHandler(logging.Handler):
    """Logging handler that logs to the posgres database."""

    def __init__(self, session):
        """
        Create a LoggingHandler object.

        :param session: sessionmaker object
        """
        logging.Handler.__init__(self)
        self.session = session

    def emit(self, record):
        """
        Store log in database.

        :param record: record object that stores the information about the log
        """
        time_created = time.strftime("%Y-%m-%d %H:%M:%S",
                                     time.localtime(record.created))
        Log.insert_log(self.session, str(record.levelno),
                       str(record.levelname), str(record.pathname),
                       record.lineno, str(record.msg.strip()), time_created,
                       str(record.name))
