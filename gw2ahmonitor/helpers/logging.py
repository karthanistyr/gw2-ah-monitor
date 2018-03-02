import logging
import logging.handlers

class LoggingHelper:
    logging_is_initiated = False
    logger_name = "ah-monitor"
    log_file = "%s.log" % logger_name

    def init_logging():
        if(not LoggingHelper.logging_is_initiated):
            logger = logging.getLogger(LoggingHelper.logger_name)
            logger.setLevel(logging.INFO)
            handler = logging.handlers.RotatingFileHandler(
                filename=LoggingHelper.log_file, delay=True)
            formatter = logging.Formatter(
                "%(asctime)s %(name)s [%(levelname)s]: %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            logging_is_initiated = True

    ### Aliases to various logger functions to hide the instance retrieval
    def critical(message):
        """Alias to logging.getLogger(logger_name).critical(message)"""
        logging.getLogger(LoggingHelper.logger_name).critical(message)

    def debug(message):
        """Alias to logging.getLogger(logger_name).debug(message)"""
        logging.getLogger(LoggingHelper.logger_name).debug(message)

    def error(message):
        """Alias to logging.getLogger(logger_name).error(message)"""
        logging.getLogger(LoggingHelper.logger_name).error(message)

    def info(message):
        """Alias to logging.getLogger(logger_name).info(message)"""
        logging.getLogger(LoggingHelper.logger_name).info(message)

    def warn(message):
        """Alias to logging.getLogger(logger_name).warn(message)"""
        logging.getLogger(LoggingHelper.logger_name).warn(message)
