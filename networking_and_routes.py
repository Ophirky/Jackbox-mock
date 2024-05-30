"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 25/04/24
    DESCRIPTION: This is the main file for the project rewrite using the new HTTP library.
"""
import logging
import threading
import inspect

import quiplash

threading_lock_backup = threading.Lock

# Logger #
LOGGER = logging.getLogger("routes_log")


class CustomLock:
    def __init__(self):
        self.lock = threading_lock_backup()

    def get_bc(self) -> str:
        if consts.GLOBAL_LOG_LEVEL == logging.DEBUG:
            return ' <- '.join(v.function for v in inspect.stack()[1:])
        return ''

    def locked(self):
        return self.lock.locked()

    def acquire(self, blocking=True, timeout=-1):
        stack = self.get_bc()
        if consts.GLOBAL_LOG_LEVEL == logging.DEBUG:
            print("Trying to acquire lock from " + stack)
        result = self.lock.acquire(blocking, timeout)
        if consts.GLOBAL_LOG_LEVEL == logging.DEBUG:
            print("Got lock for " + stack)
        return result

    def release(self):
        self.lock.release()
        if consts.GLOBAL_LOG_LEVEL == logging.DEBUG:
            print("Released lock for " + self.get_bc())

    def __enter__(self):
        stack = self.get_bc()
        if consts.GLOBAL_LOG_LEVEL == logging.DEBUG:
            print("Trying to acquire lock from " + stack)
        res = self.lock.__enter__()
        if consts.GLOBAL_LOG_LEVEL == logging.DEBUG:
            print("Got lock for " + stack)
        return res

    def __exit__(self, exc_type, exc_val, exc_tb):
        if consts.GLOBAL_LOG_LEVEL == logging.DEBUG:
            print("Released lock for " + self.get_bc())
        return self.lock.__exit__(exc_type, exc_val, exc_tb)


threading.Lock = CustomLock

import time
import httpro
from quiplash import game_constants as gconsts
from utils.decorators import lock_game_manager
from quiplash.player import Player
from utils import general_constants as consts
from utils.global_vars import app, game_manager, round_time_seconds, game_manager_lock
import utils.global_vars
from quiplash.protocol import QuiplashProtocol


def increase_submition_counter() -> int:
    """
    Increases the submition counter
    :return int: The submission counter.
    """
    res = -1
    if game_manager_lock.locked():
        utils.global_vars.game_manager.submission_counter += 1
        LOGGER.debug(f"submission_counter = {utils.global_vars.game_manager.submission_counter}")
        res = utils.global_vars.game_manager.submission_counter
    return res


def handle_sentence_submition(player: Player, submition: str) -> None:
    """
    Handles the player sentence submition
    :param player: The player that submitted
    :param submition: the submitted sentence.
    :return: None
    """
    player.answer = submition
    increase_submition_counter()


def handle_vote_submission(submition: str, player: Player) -> None:
    """
    Handles the vote submission.
    :param submition: The submission (a or b)
    :param player: The player who voted
    :return: None
    """
    player.voted = True
    with utils.global_vars.sentence_division_lock:
        utils.global_vars.sentence_division[list(utils.global_vars.sentence_division.keys())[
            game_manager.current_sentence_vote]][
            int(submition)].voting_score += 1

    increase_submition_counter()


def new_player(username: bytes) -> None:
    """
    This function is responsible for adding the new player to the player list.
    :param username: The username of the new player.
    :return: None
    """
    game_manager.players.append(Player(username))
    if len(game_manager.players) == gconsts.NUMBER_OF_PLAYERS_TO_START:
        game_manager.game_started = True


# Non page requests #
@app.route(b"/start-vote")
@lock_game_manager
def start_sentence_vote(request: httpro.http_parser.HttpParser) -> httpro.http_message.HttpMsg:
    """
    This will handle the routing to the voting/game-over page.
    :param request: The request from the client.
    :return: The html request for the correct page or 200 for game not started.
    """
    return_val = httpro.http_message.HttpMsg(content_type=httpro.constants.MIME_TYPES["sse"],
                                             body=b"data: %b\n\n" % QuiplashProtocol.format(start_game=False))

    if game_manager.current_scene == gconsts.VOTING_SCENE_INDEX:
        for player in game_manager.players:
            if player.username == request.COOKIES[b"username"].decode() \
                    and not player.voted and not game_manager.game_over:
                return_val = httpro.http_message.HttpMsg(content_type=httpro.constants.MIME_TYPES["sse"],
                                                         body=b"data: %b\n\n" % QuiplashProtocol.format(
                                                             start_game=True,
                                                             location="vote.html"))
    elif game_manager.game_over:
        return_val = httpro.http_message.HttpMsg(content_type=httpro.constants.MIME_TYPES["sse"],
                                                 body=b"data: %b\n\n" % QuiplashProtocol.format(
                                                     start_game=True,
                                                     location="game-over.html"))

    return return_val


@app.route(b"/username")
@lock_game_manager
def username_check(request: httpro.http_parser.HttpParser) -> httpro.http_message.HttpMsg:
    """
    Handles the user logi-n
    :param request: The request for the page.
    :return httpro.http_message.HttpMsg: if the username is valid.
    """
    username = QuiplashProtocol.deformat(request.BODY.decode())["txt"]

    if game_manager.game_started:
        response = httpro.http_message.HttpMsg(location="forbidden.html")
    elif username not in game_manager.players:
        new_player(username)
        response = httpro.http_message.HttpMsg(location="waiting-lounge.html", set_cookie="username=" + username)
    else:
        response = httpro.http_message.HttpMsg(error_code=500)

    return response


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
                                               body=b"data: %b\n\n" % QuiplashProtocol.format(start_game=True))
    else:
        response = httpro.http_message.HttpMsg(content_type="text/event-stream",
                                               body=b"data: %b\n\n" % QuiplashProtocol.format(start_game=False))
    return response


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
        with utils.global_vars.sentence_division_lock:
            for sentence, players in utils.global_vars.sentence_division.items():
                # If sentence found #
                if username.decode() in [player.username for player in players]:
                    time_left_for_game = utils.global_vars.round_start_time + round_time_seconds - time.time()
                    protocol_res = QuiplashProtocol.format(txt=sentence % "___", time_left=time_left_for_game)

                    return_value = httpro.http_message.HttpMsg(content_type=httpro.constants.MIME_TYPES["sse"],
                                                               body=b'data: %s\n\n' % protocol_res)
                    break

    return return_value


@app.route(b"/submit")
@lock_game_manager
def get_answer_from_user(request: httpro.http_parser.HttpParser) -> httpro.http_message.HttpMsg:
    """
    Gets the answer from a player and adds it to the answers dict
    :param request: The player's answer
    :return httpro.http_message.HttpMsg: confirm message that the sentence was received.
    """
    return_value = httpro.http_message.HttpMsg(error_code=404)  # is the user wasn't found.
    if game_manager.current_scene != gconsts.SENTENCE_INPUT_SCENE_INDEX \
            and game_manager.current_scene != gconsts.VOTING_SCENE_INDEX:
        LOGGER.debug("The scene is not correct.")
        return_value = httpro.http_message.HttpMsg(error_code=403, content_type=httpro.constants.MIME_TYPES[".html"],
                                                   body=httpro.read_file(gconsts.FORBIDDEN_PATH))
    else:
        username = request.COOKIES[b"username"]

        # Find the sentence assigned to the player #
        for player in utils.global_vars.game_manager.players:
            # If player found #
            if username.decode() == player.username:
                if game_manager.current_scene == gconsts.SENTENCE_INPUT_SCENE_INDEX and not player.answer:
                    handle_sentence_submition(player, QuiplashProtocol.deformat(request.BODY.decode())["txt"])
                    return_value = httpro.http_message.HttpMsg()

                # If submitted a vote #
                elif game_manager.current_scene == gconsts.VOTING_SCENE_INDEX and not player.voted:
                    # Add score to the player that got the votes #
                    handle_vote_submission(QuiplashProtocol.deformat(request.BODY.decode())["txt"], player)
                    return_value = httpro.http_message.HttpMsg()

                break

            else:
                return_value = httpro.http_message.HttpMsg(error_code=403,
                                                           content_type=httpro.constants.MIME_TYPES[".html"],
                                                           body=httpro.read_file(gconsts.FORBIDDEN_PATH))

    return return_value


# Page requests #
@app.route(b"/")
def home_page(request: httpro.http_parser.HttpParser) -> httpro.http_message.HttpMsg:
    """
    Home page for the game - log in
    :param request: The request for the page.
    :return httpro.http_message.HttpMsg: The html for the index.html file.
    """
    return httpro.http_message.HttpMsg(content_type=httpro.constants.MIME_TYPES[".html"],
                                       body=httpro.read_file(gconsts.HOME_PAGE_PATH))


@app.route(b"/forbidden.html")
def forbidden_page(request: httpro.http_parser.HttpParser) -> httpro.http_message.HttpMsg:
    """
    A route to the forbidden html page.
    :param request: The client request.
    :return: The html for the 403 forbidden page.
    """
    return httpro.http_message.HttpMsg(content_type=httpro.constants.MIME_TYPES[".html"],
                                       body=httpro.read_file(gconsts.FORBIDDEN_PATH))


@app.route(b"/vote.html")
@lock_game_manager
def vote_page(request: httpro.http_parser.HttpParser) -> httpro.http_message.HttpMsg:
    """
    Gives the client the voting page.
    :param request: The client request
    :return: http message containing the appropriate html code.
    """
    return_val = httpro.http_message.HttpMsg(error_code=403, content_type=httpro.constants.MIME_TYPES[".html"],
                                             body=httpro.read_file(gconsts.FORBIDDEN_PATH))
    if game_manager.current_scene == gconsts.VOTING_SCENE_INDEX:
        return_val = httpro.http_message.HttpMsg(content_type=httpro.constants.MIME_TYPES[".html"],
                                                 body=httpro.read_file(gconsts.VOTING_PAGE_FILE_PATH))
    return return_val


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
    The page that the players will enter the sentences to.
    :param request: The request for the page.
    :return httpro.http_message.HttpMsg: round one html.
    """
    return_value = None
    if not game_manager.current_scene == gconsts.SENTENCE_INPUT_SCENE_INDEX:
        return_value = httpro.http_message.HttpMsg(error_code=403, content_type=httpro.constants.MIME_TYPES[".html"],
                                                   body=httpro.read_file(gconsts.FORBIDDEN_PATH))
    else:
        return_value = httpro.http_message.HttpMsg(content_type=httpro.constants.MIME_TYPES[".html"],
                                                   body=httpro.read_file(gconsts.ROUND_ONE_FILE_PATH))
    return return_value


@app.route(b"/game-over.html")
def game_over_page(request: httpro.http_parser.HttpParser) -> httpro.http_message.HttpMsg:
    """
    The game over page.
    :param request: The request for the page.
    :return httpro.http_message.HttpMsg: round one html.
    """
    return httpro.http_message.HttpMsg(content_type=httpro.constants.MIME_TYPES[".html"],
                                       body=httpro.read_file(gconsts.GAME_OVER_PAGE_PATH))

def network_setup() -> None:
    """
    Setting up the logger.
    :return: None
    """
    # Main logger setup #
    LOGGER.setLevel(consts.GLOBAL_LOG_LEVEL)
    file_handler = logging.FileHandler(consts.MAIN_LOG)
    file_handler.setFormatter(logging.Formatter(consts.GLOBAL_LOG_FORMAT))
    LOGGER.addHandler(file_handler)

    # 404 page setup #
    app.set_four_o_four(quiplash.consts.NOT_FOUND_PAGE)
