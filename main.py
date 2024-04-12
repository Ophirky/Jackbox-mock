"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 16/03/24
    DESCRIPTION: The main file of the project - the file that needs to be run.
"""
# Imports #
import logging
import os.path
import select
import socket
import re
import json

import games.game_manager
import http_ophir

from games import Player
import usefull_files.general_constants as consts

# Global Vars #
global readable_socks_list, writeable_socks_list, exception_socks_list
players = []
game_started = False
response: http_ophir.http_message.HttpMsg


# Log initialization handling #
def log_init_handler() -> None:
    """
    Handlers all the logging initialization process
    :return: None
    """
    if not os.path.isdir(consts.LOG_DIR):
        os.makedirs(consts.LOG_DIR)

    logging.basicConfig(level=consts.LOG_LEVEL, filename=consts.MAIN_LOG, format=consts.LOG_FORMAT)


def auto_test_main() -> None:
    """
    This function includes all the auto checks of the project
    :return: None
    """
    http_ophir.http_auto_tests()
    logging.info(consts.TESTS_RUN)


def receive_message(client_socket: socket) -> bool or http_ophir.http_parser.HttpParser:
    """
    Receives a message from a client
    :param client_socket:
    :return bool or http_ophir.http_parser.HttpParser: False if the message is invalid, HttpParser with the message
    """
    try:
        message = client_socket.recv(consts.RECV_LENGTH)

        while b"\r\n\r\n" not in message:
            msg = client_socket.recv(consts.RECV_LENGTH)
            if not msg:
                break
            message += msg

        try:
            content_length = int(re.search(rb'Content-Length: (\d+)', message).group(1))

            # Check if body was already received #
            if len(message.split(b'\r\n\r\n')) > 1 and len(message.split(b'\r\n\r\n')[1]) != content_length:
                body = b''
                # Receiving body #
                while len(body) < content_length:
                    chunk = client_socket.recv(consts.RECV_LENGTH)
                    if not chunk:
                        break
                    body += chunk

                message += body

        except AttributeError:
            logging.info(consts.NO_CONTENT_HEADER)

        except Exception as e:
            logging.exception(e)

        return http_ophir.http_parser.HttpParser(message)

    except Exception as e:
        logging.exception(e)


def new_player(username: bytes) -> None:
    """
    This function is responsible for adding the new player to the player list.
    :param username: The username of the new player.
    :return: None
    """
    global game_started
    players.append(Player.Player(username))
    if len(players) == 4:
        game_started = True


def user_login_handler(uri: bytes, request: http_ophir.http_parser.HttpParser) -> None:
    """
    Handles the user log-in requests
    :param uri: The request uri
    :param request: the request itself
    :return: None
    """
    if uri.startswith(b"/username"):
        global response
        username = json.loads(request.BODY.decode("utf-8"))["username"]
        if game_started:
            response = http_ophir.http_message.HttpMsg(location="/game-started.html")
        elif username not in players:
            new_player(username)
            response = http_ophir.http_message.HttpMsg(location="/waiting_lounge.html")
        else:
            response = http_ophir.http_message.HttpMsg(error_code=500)
    # Start the game #
    if game_started:
        games.game_manager.game_manager(players)


def handle_client(request: http_ophir.http_parser.HttpParser, client_socket: socket, client_addr: list) -> None:
    """
    This function handles the client requests and responses
    :param client_addr: The ip and port of the client.
    :param request: The client message.
    :param client_socket: The client socket.
    :return: None
    """
    global response
    uri = request.URI

    # fixing uri #
    if uri == b"/":
        uri = b"/index.html"

    logging.debug(request.HTTP_REQUEST)

    if request.METHOD == b"POST":
        # Username entry before game #
        user_login_handler(uri, request)

    elif request.METHOD == b"GET":
        # Client checks if the game has started #
        if uri.startswith(b"/did-start"):
            if game_started:

                response = http_ophir.http_message.HttpMsg(content_type="text/event-stream",
                                                           body=b"data: {\"start-game\": \"%s\"}\n\n" % b"Hello Bro")
            else:
                response = http_ophir.http_message.HttpMsg(content_type="text/event-stream",
                                                           body=b"data: \n\n")

        # If the requested file is not in the website root folder #
        elif not os.path.isfile(consts.ROOT_DIRECTORY + uri):
            with open(consts.FOUR_O_FOUR, 'rb') as file:
                response = http_ophir.http_message.HttpMsg(error_code=404,
                                                           content_type=http_ophir.constants.MIME_TYPES[".html"],
                                                           body=file.read())
        # If uri does not have a special path #
        else:
            # extract requested file type from URL (html, jpg etc)
            file_type = os.path.splitext(uri)[1]

            # generate proper HTTP header
            file_data: bytes
            with open(consts.ROOT_DIRECTORY + uri, 'rb') as f:
                file_data = f.read()
            response = http_ophir.http_message.HttpMsg(content_type=http_ophir.constants.MIME_TYPES[file_type.decode()],
                                                       body=file_data)

    # Send the final message to the client #
    client_socket.send(response.build_message_bytes())


# Main Function #
def main() -> None:
    """
    The main function of the project
    :return: None
    """
    global readable_socks_list, writeable_socks_list, exception_socks_list

    # Setting up the socket #
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((consts.IP, consts.PORT))
    sock.listen()

    socket_list = [sock]

    try:
        while True:
            readable_socks_list, writeable_socks_list, exception_socks_list = select.select(socket_list, socket_list,
                                                                                            socket_list)

            for notified_socket in readable_socks_list:
                if notified_socket == sock:  # checking for new connection #
                    client_socket, client_addr = sock.accept()
                    try:
                        logging.info(consts.NEW_CLIENT.format(client_addr[0], client_addr[1]))

                        message: http_ophir.http_parser.HttpParser = receive_message(client_socket)
                        handle_client(message, client_socket, client_addr)

                    except Exception as e:
                        logging.exception(e)

                    finally:
                        client_socket.close()
    finally:
        sock.close()


if __name__ == '__main__':
    # Log handling #
    log_init_handler()

    # Auto tests #
    auto_test_main()

    # Main program #
    main()
