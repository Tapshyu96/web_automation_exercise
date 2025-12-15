import logging

class LogMaker:
    @staticmethod
    def log_gen():
        logging.basicConfig(filename=".\\logs\\automationexercise.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', force=True)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        return logger