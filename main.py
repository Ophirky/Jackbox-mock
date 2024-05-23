"""

"""
import networking_and_routes as nar
import quiplash
import httpro
import os
import utils.general_constants as consts
import logging
import threading

if __name__ == '__main__':
    # Main logging file init
    if not os.path.isdir(consts.GLOBAL_LOG_DIR):
        os.makedirs(consts.GLOBAL_LOG_DIR)

    # Asserts and setup #
    httpro.http_setup()
    quiplash.quiplash_setup()
    nar.network_setup()

    # Thread setup #
    socket_thread = threading.Thread(target=nar.app.run)
    game_socket = threading.Thread(target=quiplash.game_main.main)

    socket_thread.start()
    game_socket.start()

    while socket_thread.is_alive() or game_socket.is_alive():
        ...
