"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 04/05/24
    DESCRIPTION: On Quiplash import. Holds asserts and log setup
"""
from quiplash import game_manager, protocol, game_main
from quiplash import game_constants as consts
from utils import general_constants as global_consts
import logging

def quiplash_setup() -> None:
    """
    Running the auto tests and sets up logger
    ! No need to check for log dir because when function is called it will already be checked !
    :return: None
    """
    game_manager.game_manager_auto_asserts()
    protocol.protocol_auto_tests()

    # Start logger #

    consts.LOGGER.setLevel(global_consts.GLOBAL_LOG_LEVEL)
    file_handler = logging.FileHandler(consts.LOG_FILE_NAME)
    file_handler.setFormatter(logging.Formatter(global_consts.GLOBAL_LOG_FORMAT))
    consts.LOGGER.addHandler(file_handler)

    consts.LOGGER.info("quiplash initiated")
