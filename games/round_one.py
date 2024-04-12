"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 07/04/24
    DESCRIPTION: This is the first round of the game.
"""
# Imports #
from games.scene import Scene
from usefull_files import general_constants as consts
import games.game_manager


# Scene #
class RoundOne(Scene):

    def __init__(self, players):
        super().__init__(consts.WHITE)
        self.players = players

    def scene(self) -> None:
        print("Alright! let's get it started!")
        sentences = games.game_manager.assign_sentences(players=self.players, sentences=consts.GAME_PROMPTS)

