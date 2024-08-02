import logging


class ProjectLogger:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',)
