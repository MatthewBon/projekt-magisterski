import logging


class ProjectLogger:
    """
    A base class that sets up logging for derived classes.

    This class provides a basic logger with a predefined format and log level.
    It also suppresses unnecessary logging from certain third-party libraries.
    """

    def __init__(self):
        """
        Initialize the ProjectLogger.

        This constructor sets up a logger for the class that derives from this base class.
        The logger's level is set to INFO by default, and the log format includes the timestamp,
        log level, and message. It also suppresses logging from 'matplotlib.font_manager' and 'PIL'
        to avoid cluttering the log output with unnecessary warnings.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # Suppress unnecessary logging from third-party libraries
        logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)
        logging.getLogger('PIL').setLevel(logging.WARNING)
