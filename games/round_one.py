"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 07/04/24
    DESCRIPTION: This is the first round of the game.
"""
import games.game_manager
# Imports #
from games.scene import Scene
from usefull_files import general_constants as consts

# Scene #
class RoundOne(Scene):

    def __init__(self):
        super().__init__(consts.WHITE)

    def scene(self) -> None:
        print("Alright! let's get it started!")
        sentences = games.game_manager.assign_sentences()
        print(sentences)
