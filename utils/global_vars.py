"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 04/05/24
    DESCRIPTION: Global variables for the project.
"""

import httpro
from quiplash.game_manager import GameManager
from quiplash.game_constants import ROUND_TIME_SECONDS_DEFAULT
from threading import Lock

app = httpro.app.App()
game_manager = GameManager()
game_manager_lock = Lock()

sentence_division = None
sentence_division_lock = Lock()

current_scene_instance = None
current_scene_instance_lock = Lock()

round_time_seconds = ROUND_TIME_SECONDS_DEFAULT

# variable has no lock since it cannot be accessed from two threads at the same time #
round_start_time = None

