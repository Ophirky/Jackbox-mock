"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 04/05/24
    DESCRIPTION: Global variables for the project.
"""

import httpro
from quiplash.game_manager import GameManager
from quiplash.game_constants import ROUND_TIME_SECONDS_DEFAULT, WINDOW_WIDTH, WINDOW_HEIGHT, FONT_PATH, TITLE_FONT_SIZE
from threading import Lock
import pygame

app = httpro.app.App()
game_manager = GameManager()
game_manager_lock = Lock()

sentence_division = None
sentence_division_lock = Lock()

current_scene_instance = None
current_scene_instance_lock = Lock()

round_time_seconds = ROUND_TIME_SECONDS_DEFAULT

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.font.init()  # Init the font at the start of the game.
text_font = pygame.font.Font(FONT_PATH, TITLE_FONT_SIZE)

# Thread Setup #
socket_thread = None  # Initialize in main.py

# variable has no lock since it cannot be accessed from two threads at the same time #
round_start_time = None
