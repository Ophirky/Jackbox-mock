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


HOME_PAGE_PATH = r"quiplash/html/index.html"
WAITING_LOUNGE_FILE_PATH = r"quiplash/html/waiting_lounge.html"
NOT_FOUND_PAGE = r"quiplash/html/404.html"
FORBIDDEN_PATH = r"quiplash/html/403.html"
ROUND_ONE_FILE_PATH = r"quiplash/html/sentence_input.html"

WAITING_LOUNGE_SCENE_INDEX = 0
EXPLANATION_SCENE_INDEX = 1
SENTENCE_INPUT_SCENE_INDEX = 2
VOTING_SCENE_INDEX = 3

ROUND_TIME_SECONDS_DEFAULT = 120

NUMBER_OF_PLAYERS_TO_START = 2

GAME_PROMPTS = (
    "I couldn't believe my eyes when I saw %s.",
    "The last thing I want to see is %s.",
    "My secret talent is %s.",
    "The title of my autobiography would be 'The Life and Times of %s.'",
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
    "There is nothing I love more than %s"
)
