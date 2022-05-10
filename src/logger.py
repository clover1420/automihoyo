import logging

class Log():
    def __init__(self) -> None:
        logging.basicConfig(format = '[%(asctime)s][%(levelname)s]:%(message)s',level=logging.INFO,)
    
    def info(self,msg) -> None:
        logging.info(msg)

    def debug(self,msg) -> None:
        logging.debug(msg)

    def error(self,msg) -> None:
        logging.error(msg)
    
    def warning(self,msg) -> None:
        logging.warning(msg)

    def critical(self,msg) -> None:
        logging.critical(msg)
    