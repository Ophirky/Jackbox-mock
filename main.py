"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 25/04/24
    DESCRIPTION: This is the main file for the project rewrite using the new HTTP library.
"""
import httpro
from quiplash import game_constants as gconsts
from utils.decorators import lock_game_manager
from quiplash.player import Player
import json
from utils.global_vars import app, game_manager, sentence_division_lock, round_time_seconds
import utils.global_vars
from quiplash import game_main
import threading
import time


def new_player(username: bytes) -> None:
    """
    This function is responsible for adding the new player to the player list.
    :param username: The username of the new player.
    :return: None
    """
    game_manager.players.append(Player(username))
    if len(game_manager.players) == gconsts.NUMBER_OF_PLAYERS_TO_START:
        game_manager.game_started = True


@app.route(b"/")
def home_page(request: httpro.http_parser.HttpParser) -> httpro.http_message.HttpMsg:
    """
    Home page for the game - log in
    :param request: The request for the page.
    :return httpro.http_message.HttpMsg: The html for the index.html file.
    """
    return httpro.http_message.HttpMsg(content_type=httpro.constants.MIME_TYPES[".html"],
                                       body=httpro.read_file(gconsts.HOME_PAGE_PATH))


@app.route(b"/did-start")
@lock_game_manager
def did_start_check(request: httpro.http_parser.HttpParser) -> httpro.http_message.HttpMsg:
    """
    way for users to check if the game started.
    :param request: The request for the page.
    :return httpro.http_message.HttpMsg: Returns if the game starts.
    """
    if game_manager.current_scene == gconsts.SENTENCE_INPUT_SCENE_INDEX:
        response = httpro.http_message.HttpMsg(content_type="text/event-stream",
                                               body=b"data: {\"start-game\": \"%s\"}\n\n" % b"true")
    else:
        response = httpro.http_message.HttpMsg(content_type="text/event-stream",
                                               body=b"data: {\"start-game\": \"%s\"}\n\n" % b"false")
    return response


@app.route(b"/username")
@lock_game_manager
def username_check(request: httpro.http_parser.HttpParser) -> httpro.http_message.HttpMsg:
    """
    Handles the user logi-n
    :param request: The request for the page.
    :return httpro.http_message.HttpMsg: if the username is valid.
    """
    username = json.loads(request.BODY.decode("utf-8"))["txt"]

    if game_manager.game_started:
        response = httpro.http_message.HttpMsg(location="game-started.html")
    elif username not in game_manager.players:
        new_player(username)
        response = httpro.http_message.HttpMsg(location="waiting-lounge.html", set_cookie="username=" + username)
    else:
        response = httpro.http_message.HttpMsg(error_code=500)

    return response


@app.route(b"/waiting-lounge.html")
def waiting_lounge_page(request: httpro.http_parser.HttpParser) -> httpro.http_message.HttpMsg:
    """
    Page where players wait for the game to start.
    :param request: The request for the page.
    :return httpro.http_message.HttpMsg: Waiting lounge html.
    """
    return httpro.http_message.HttpMsg(content_type=httpro.constants.MIME_TYPES[".html"],
                                       body=httpro.read_file(gconsts.WAITING_LOUNGE_FILE_PATH))


@app.route(b"/sentence-input.html")
def sentence_input_page(request: httpro.http_parser.HttpParser) -> httpro.http_message.HttpMsg:
    """
    :param request: The request for the page.
    :return httpro.http_message.HttpMsg: round one html.
    """
    return_value = None
    if not game_manager.current_scene == gconsts.SENTENCE_INPUT_SCENE_INDEX:
        return_value = httpro.http_message.HttpMsg(error_code=403, content_type=httpro.constants.MIME_TYPES[".html"],
                                                   body=httpro.read_file(gconsts.FORBIDDEN_PATH))
    else:
        return_value = httpro.http_message.HttpMsg(conten_type=httpro.constants.MIME_TYPES[".html"],
                                                   body=httpro.read_file(gconsts.ROUND_ONE_FILE_PATH))
    return return_value


@app.route(b"/get-sentence")
@lock_game_manager
def get_sentence_request(request: httpro.http_parser.HttpParser) -> httpro.http_message.HttpMsg:
    """
    Sends a player his sentence and the time remaining to game.
    :param request: The player's request
    :return httpro.http_message.HttpMsg: sentence and the time remaining to game
    """
    return_value = httpro.http_message.HttpMsg(error_code=500)
    if not game_manager.current_scene == gconsts.SENTENCE_INPUT_SCENE_INDEX:
        return_value = httpro.http_message.HttpMsg(error_code=403, content_type=httpro.constants.MIME_TYPES[".html"],
                                                   body=httpro.read_file(gconsts.FORBIDDEN_PATH))
    else:
        username = request.COOKIES[b"username"]

        # Find the sentence assigned to the player #
        for sentence, players in utils.global_vars.sentence_division.items():
            # If sentence found #
            if username.decode() in [player.username for player in players]:
                time_left_for_game = utils.global_vars.round_start_time + round_time_seconds - time.time()
                protocol_res = json.dumps({"txt": sentence % "___", "time-left": str(time_left_for_game)})

                return_value = httpro.http_message.HttpMsg(content_type=httpro.constants.MIME_TYPES["sse"],
                                                           body=b'data: %s\n\n' % protocol_res.encode())
                break

    return return_value


# TODO: Check if works.
@app.route(b"/send-sentence")
def get_answer_from_user(request: httpro.http_parser.HttpParser) -> httpro.http_message.HttpMsg:
    """
    Gets the answer from a player and adds it to the answers dict
    :param request: The player's answer
    :return httpro.http_message.HttpMsg: confirm message that the sentence was received.
    """
    return_value = httpro.http_message.HttpMsg(error_code=404)  # is the user wasn't found.
    if game_manager.current_scene != gconsts.SENTENCE_INPUT_SCENE_INDEX:
        return_value = httpro.http_message.HttpMsg(error_code=403, content_type=httpro.constants.MIME_TYPES[".html"],
                                                   body=httpro.read_file(gconsts.FORBIDDEN_PATH))
    else:
        username = request.COOKIES[b"username"]

        # Find the sentence assigned to the player #
        for player in utils.global_vars.game_manager.players:
            # If sentence found #
            if username.decode() == player.username:
                player.answer = request.BODY.decode()["txt"]
                return_value = httpro.http_message.HttpMsg()
                break

    return return_value


if __name__ == '__main__':
    # Asserts #
    httpro.http_auto_tests()

    # 404 page setup #
    app.set_four_o_four(gconsts.NOT_FOUND_PAGE)

    # Thread setup #
    socket_thread = threading.Thread(target=app.run)
    game_socket = threading.Thread(target=game_main.main)

    socket_thread.start()
    game_socket.start()

    while socket_thread.is_alive() or game_socket.is_alive():
        pass
