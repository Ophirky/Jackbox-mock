"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 25/04/24
    DESCRIPTION: Constants for the game.
"""
import logging
from utils.general_constants import GLOBAL_LOG_DIR

# Logging #
LOG_FILE_NAME = GLOBAL_LOG_DIR + r"\quiplash_logs.log"
QUIPLASH_LOGGER_NAME = "quip_log"
LOGGER = logging.getLogger(QUIPLASH_LOGGER_NAME)

ROOT_DIR = r"quiplash/"
HOME_PAGE_PATH = ROOT_DIR + r"html/index.html"
WAITING_LOUNGE_FILE_PATH = ROOT_DIR + r"html/waiting_lounge.html"
NOT_FOUND_PAGE = ROOT_DIR + r"html/404.html"
FORBIDDEN_PATH = ROOT_DIR + r"html/403.html"
ROUND_ONE_FILE_PATH = ROOT_DIR + r"html/sentence_input.html"
VOTING_PAGE_FILE_PATH = ROOT_DIR + r"html/vote.html"
GAME_OVER_PAGE_PATH = ROOT_DIR + r"html/game_over.html"

FONT_PATH = r"quiplash/static/fonts/GROBOLD.ttf"
FAVICON_PATH = r"quiplash/static/imgs/favicon.ico"
TITLE_FONT_SIZE = 64

COLOR_WHITE = 'white'

WAITING_LOUNGE_SCENE_INDEX = 0
SENTENCE_INPUT_SCENE_INDEX = 1
VOTING_SCENE_INDEX = 2

ROUND_TIME_SECONDS_DEFAULT = 120

NUMBER_OF_PLAYERS_TO_START = 2

GAME_PROMPTS = (
    "The title of my autobiography would be 'The Life and Times of %s.'",
    "I couldn't believe my eyes when I saw %s.",
    "The last thing I want to see is %s.",
    "My secret talent is %s.",
    "If I could have any superpower, it would be %s.",
    "The most surprising thing I learned yesterday was %s.",
    "My favorite hobby is %s.",
    "If I could live anywhere in the world, it would be %s.",
    "The one thing I can't live without is %s.",
    "My biggest fear is %s.",
    "The most unusual thing in my house is %s.",
    "If I were an animal, I would be a %s.",
    "My favorite movie of all time is %s.",
    "The best piece of advice I've ever received is %s.",
    "If I could meet anyone, living or dead, it would be %s.",
    "The most interesting fact I know is %s.",
    "If I could go back in time, I would visit %s.",
    "My dream job is %s.",
    "The funniest joke I know is %s.",
    "The most beautiful place I've ever been is %s.",
    "A new TV show called \"MommyFight\" is about %s",
    "FluffyPoofs is a name for a new %s",
    "Tell me something I don't know. %s",
    "My mom told that she %s",
    "There is nothing I love more than %s",
    "I want to meet the queen of england because %s.",
    "I want to eat %s it will be cool."
)

# Pygame Consts #
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
