"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 03/05/24
    DESCRIPTION: Handles the server side front-end
"""
import time
import quiplash.waiting_lounge as wait_lounge
import quiplash.explanation_of_game as explain
from quiplash import player_sentences
from utils import global_vars
from quiplash.scene import Scene

# Constants #
SCENE_ORDER = (wait_lounge.WaitingLounge, explain.Explanation, player_sentences.PlayerSentences)

# variables init #
explanation_scene = None


def run_scene(scene) -> None:
    """
    Executes a scene in the game
    :param scene: The scene to run
    :return: None
    """

    scene.scene()


def main() -> None:
    """
    The game's main program (scene handler)
    :return: None
    """

    # Initializing the first scene #
    global_vars.current_scene_instance = SCENE_ORDER[global_vars.game_manager.current_scene]()

    while True:
        # Thread delay #
        time.sleep(0.01)

        # Lock game manager #
        with global_vars.game_manager_lock:
            # run the scene #
            run_scene(global_vars.current_scene_instance)

            # Move to scene #1 condition - game explanation #
            if (
                    (global_vars.game_manager.game_started and global_vars.game_manager.current_scene == 0)
                    or global_vars.current_scene_instance.scene_over
            ) and global_vars.game_manager.current_scene < len(SCENE_ORDER) - 1:
                global_vars.game_manager.next_scene()
                global_vars.current_scene_instance = SCENE_ORDER[global_vars.game_manager.current_scene]()
