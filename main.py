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

import http_ophir
import usefull_files.general_constants as consts

# Global Vars #
global readable_socks_list, writeable_socks_list, exception_socks_list
players = dict()


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

        except Exception as e:
            logging.info(e)

        return http_ophir.http_parser.HttpParser(message)

    except Exception as e:
        logging.exception(e)


def new_player(username: bytes, address: bytes):
    players[address] = username
    print(players)


def handle_client(request: http_ophir.http_parser.HttpParser, client_socket: socket, client_addr: list) -> None:
    """
    This function handles the client requests and responses
    :param client_addr: The ip and port of the client.
    :param request: The client message.
    :param client_socket: The client socket.
    :return: None
    """
    uri = request.URI
    response: http_ophir.http_message.HttpMsg

    # fixing uri #
    if uri == b"/":
        uri = b"/index.html"
    logging.debug(request.HTTP_REQUEST)
    if request.METHOD == b"POST":
        # Username entry before game #
        if uri.startswith(b"/username"):
            with open(consts.ROOT_DIRECTORY + b"/waiting_lounge.html", 'rb') as f:
                response = http_ophir.http_message.HttpMsg(location="/waiting_lounge.html")
            if client_addr not in players:
                new_player(json.loads(request.BODY.decode("utf-8"))["username"], client_addr[0])

    elif request.METHOD == b"GET":
        if not os.path.isfile(consts.ROOT_DIRECTORY + uri):
            with open(consts.FOUR_O_FOUR, 'rb') as file:
                response = http_ophir.http_message.HttpMsg(error_code=404, content_type=http_ophir.constants.MIME_TYPES[".html"],
                                                           body=file.read())
        else:

            # extract requested file type from URL (html, jpg etc)
            file_type = os.path.splitext(uri)[1]

            # generate proper HTTP header
            file_data: bytes
            with open(consts.ROOT_DIRECTORY + uri, 'rb') as f:
                file_data = f.read()
            response = http_ophir.http_message.HttpMsg(content_type=http_ophir.constants.MIME_TYPES[file_type.decode()],
                                                       body=file_data)

    client_socket.send(response.build_message_bytes())


# Main Function #
def main() -> None:
    """
    The main function of the project
    :return: None
    """
    global readable_socks_list, writeable_socks_list, exception_socks_list

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
                        logging.info("client disconnected")
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
