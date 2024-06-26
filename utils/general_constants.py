"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 16/03/24
    DESCRIPTION: File that contains all the global constants of the project.
"""
# Imports #
import logging

# Logging #
GLOBAL_LOG_LEVEL = logging.ERROR
GLOBAL_LOG_DIR = r"Logs"
GLOBAL_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"

# Log Files #
MAIN_LOG = GLOBAL_LOG_DIR + r"\main_log.log"

# Socket Related #
RECV_LENGTH = 1024
PORT = 80
IP = "127.0.0.1"

# Colors #
WHITE = (255, 255, 255)
