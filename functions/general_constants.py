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
