"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 16/03/24
    DESCRIPTION: File that contains all the global constants of the project.
"""
# Imports #
import logging

# Logging #
LOG_LEVEL = logging.DEBUG
LOG_DIR = r"Logs"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"

# Log Files #
HTTP_LOG = LOG_DIR + r"\http_logs.log"
MAIN_LOG = LOG_DIR + r"\main_log.log"

# Socket Related #
RECV_LENGTH = 1024
PORT = 80
IP = "127.0.0.1"

# Logging level - info #
NO_BODY = "Message has no body."
NEW_CLIENT = "{}:{} connected."
TESTS_RUN = "Auto tests were run."

# Website #
ROOT_DIRECTORY = b"games"
INDEX_PAGE = ROOT_DIRECTORY+b"/index.html"
FOUR_O_FOUR = ROOT_DIRECTORY+b"/404.html"
