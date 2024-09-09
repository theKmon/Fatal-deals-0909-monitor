import logging

class Logger:
    """Encapsulates the logging functionality for the entire application."""

    _instance = None  # Singleton instance for shared logging

    @staticmethod
    def get_logger():
        """Returns the shared logger instance."""
        if Logger._instance is None:
            Logger._instance = Logger._initialize_logger()
        return Logger._instance

    @staticmethod
    def _initialize_logger():
        """Initializes and configures the logger."""
        logger = logging.getLogger("ApplicationLogger")
        logger.setLevel(logging.INFO)

        if not logger.hasHandlers():  # Avoid adding multiple handlers
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
            console_handler.setFormatter(formatter)

            # Add more handlers if needed (e.g., FileHandler, etc.)
            logger.addHandler(console_handler)

        return logger

    @staticmethod
    def info(message):
        """Logs an info message."""
        logger = Logger.get_logger()
        logger.info(message)

    @staticmethod
    def error(message):
        """Logs an error message."""
        logger = Logger.get_logger()
        logger.error(message)

    @staticmethod
    def exception(message):
        """Logs an exception."""
        logger = Logger.get_logger()
        logger.exception(message)
