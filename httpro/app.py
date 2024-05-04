"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 15/04/24
    DESCRIPTION: This is the app class. It will handle the webapp and the path.
"""
import glob
# Imports #
import socket
import time

import select
import httpro.constants as consts
import logging
import re
import httpro.http_parser
import os

# global vars #
global readable_socks_list, writeable_socks_list, exception_socks_list


class App:
    """The Base for the web app."""

    # ---------- Constructor ---------- #
    def __init__(self):
        """This is the Constructor of the App class."""
        self.routes = dict()
        self.four_o_four = consts.FOUR_O_FOUR

    # ---------- Decorators ---------- #
    def route(self, route: bytes, permission_cookie: bytes = "None"):
        """
        Route decorator - adds the route to the routes' dictionary.
        :param permission_cookie: The cookie name that allows permission to page.
        :param route: the route for the uri
        :return: what the original function needs to return
        """

        def add_to_route_dict(original_function):
            """
            This is the decorator function
            :param original_function: original function that decorator decorates
            :return: what the original function needs to return
            """
            self.routes[route] = original_function, permission_cookie

            def wrapper_function(*args, **kwargs):
                """
                This is the wrapper function.
                """
                raise Exception("This is a route function. It cannot be run.")

            return wrapper_function

        return add_to_route_dict

    # ---------- Private functions ---------- #
    @staticmethod
    def __receive_message(client_socket: socket) -> bool or httpro.http_parser.HttpParser:
        """
        Receives a message from a client
        :param client_socket:
        :return bool or HttpParser: False if the message is invalid, HttpParser with the message
        """
        try:
            print("receive 1")
            message = b""

            print("received")

            # Multiple receives to eliminate server blocking without too many requests with the timeout #
            time_start = time.time()
            while b"\r\n\r\n" not in message and time.time() - time_start < consts.RECV_TIMEOUT:
                print("receiving msg")
                msg = b""
                try:
                    msg = client_socket.recv(consts.RECV_LENGTH)
                except socket.timeout:
                    pass

                if not msg:
                    continue
                message += msg

            try:
                content_length = int(re.search(rb'Content-Length: (\d+)', message).group(1))
                print(content_length)
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
                # logging.info(consts.NO_CONTENT_HEADER)
                print("errorrr")

            except Exception as e:
                # logging.exception(e)
                print(e)

            return httpro.http_parser.HttpParser(message)

        except Exception as e:
            # logging.exception(e)
            print(e)

    def __handle_client(self, request: httpro.http_parser.HttpParser, client_socket: socket) -> None:
        """
        Handles the client input.
        :param request: The request that the server got.
        :param client_socket: The client socket.
        :return: None
        """
        response: httpro.http_message

        if request.URI is not None:
            print(request.URI)
            if request.URI in self.routes.keys() and \
                    (self.routes[request.URI][1] == "None" or
                     (request.COOKIES and self.routes[request.URI][1] in request.COOKIES.keys())):
                print("Entering route function")
                response = self.routes[request.URI][0](request)
                print("Quitting")

            elif not os.path.isfile(request.URI[1:].replace(b"%20", b" ")):
                with open(self.four_o_four, 'rb') as file:
                    response = httpro.http_message.HttpMsg(error_code=404,
                                                           headers={"content_type": consts.MIME_TYPES[".html"]},
                                                           body=file.read())
            # If uri does not have a special path #
            else:
                # extract requested file type from URL (html, jpg etc)
                file_type = os.path.splitext(request.URI)[1]

                # generate proper HTTP header
                file_data: bytes
                with open(request.URI[1:].replace(b"%20", b" "), 'rb') as f:
                    file_data = f.read()
                response = httpro.http_message.HttpMsg(headers={"content_type": consts.MIME_TYPES[file_type.decode()]},
                                                       body=file_data)

            client_socket.send(response.build_message_bytes())

    # ---------- Public functions ---------- #
    def set_four_o_four(self, route: str) -> None:
        """
        Sets the route to the 404 page.
        :param route: The route to the 404 page html.
        :return: None
        """
        self.four_o_four = route

    def run(self, port=consts.PORT, host=consts.IP) -> None:
        """
        Starts the http server.
        :return: None
        """
        global readable_socks_list, writeable_socks_list, exception_socks_list

        # Setting up the socket #
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind((host, port))
        sock.listen()

        socket_list = [sock]

        try:
            while True:
                print("running")
                readable_socks_list, writeable_socks_list, exception_socks_list = select.select(socket_list,
                                                                                                socket_list,
                                                                                                socket_list)

                for notified_socket in readable_socks_list:
                    if notified_socket == sock:  # checking for new connection #
                        client_socket, client_addr = sock.accept()
                        client_socket.settimeout(.5)
                        try:
                            logging.info(consts.NEW_CLIENT.format(client_addr[0], client_addr[1]))

                            print("receiving request")
                            message: httpro.http_parser.HttpParser = self.__receive_message(client_socket)
                            print("Received Request")
                            self.__handle_client(message, client_socket)

                        except Exception as e:
                            logging.exception(e)

                        finally:
                            client_socket.close()
        finally:
            sock.close()
