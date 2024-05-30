"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 19/05/2024
    DESCRIPTION: Running the game.
"""
import networking_and_routes as nar
import quiplash
import httpro
import os
import utils.general_constants as consts
from utils import global_vars
import threading

if __name__ == '__main__':
    # Main logging file init
    if not os.path.isdir(consts.GLOBAL_LOG_DIR):
        os.makedirs(consts.GLOBAL_LOG_DIR)

    # Asserts and setup #
    httpro.http_setup()
    quiplash.quiplash_setup()
    nar.network_setup()

    # Starting the networking thread #
    global_vars.socket_thread = threading.Thread(target=nar.app.run)
    global_vars.socket_thread.start()

    # Running the pygame script in the main thread - pygame is not thread safe #
    quiplash.game_main.main()
