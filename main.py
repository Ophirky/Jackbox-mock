"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 16/03/24
    DESCRIPTION: The main file of the project - the file that needs to be run.
"""
# Imports #
import logging
import os.path
import http
import functions.general_constants as consts


# Log initialization handling #
def log_init_handler() -> None:
    """
    Handlers all the logging initialization process
    :return: None
    """
    if not os.path.isdir(consts.LOG_DIR):
        os.makedirs(consts.LOG_DIR)

    log_files = (consts.HTTP_LOG, consts.MAIN_LOG)

    for log in log_files:
        print(log)
        logging.basicConfig(level=consts.LOG_LEVEL, filename=log, format=consts.LOG_FORMAT)


def auto_test_main() -> None:
    """
    This function includes all the auto checks of the project
    :return: None
    """
    http.http_auto_tests()


# Main Function #
def main() -> None:
    """
    The main function of the project
    :return: None
    """


if __name__ == '__main__':
    # Log handling #
    log_init_handler()

    # Auto tests #
    auto_test_main()

    # Main program #
    main()
