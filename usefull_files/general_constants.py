"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 16/03/24
    DESCRIPTION: File that contains all the global constants of the project.
"""
# Imports #
import logging

# Logging #
LOG_LEVEL = logging.DEBUG
LOG_DIR = r"Logs"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"

# Log Files #
HTTP_LOG = LOG_DIR + r"\http_logs.log"
MAIN_LOG = LOG_DIR + r"\main_log.log"

# Socket Related #
RECV_LENGTH = 1024
PORT = 80
IP = "127.0.0.1"

# Logging level - info #
NO_BODY = "Message has no body."
NEW_CLIENT = "{}:{} connected."
TESTS_RUN = "Auto tests were run."
NO_CONTENT_HEADER = "The message does not have Content-Length header"

# Website #
ROOT_DIRECTORY = b"games"
INDEX_PAGE = ROOT_DIRECTORY+b"/index.html"
FOUR_O_FOUR = ROOT_DIRECTORY+b"/404.html"

# Colors #
WHITE = (255, 255, 255)

# Sentences #
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
    "A new TV show called \"MommyFight\" is about %s"
)

