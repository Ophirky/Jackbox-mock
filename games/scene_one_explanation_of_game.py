"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 07/04/24
    DESCRIPTION: This is the first scene of the game. once it is started.
"""
# Imports #
from games.scene import Scene
from usefull_files import general_constants as consts


# Scene #
class Explanation(Scene):

    def __init__(self):
        super().__init__(consts.WHITE)

    def scene(self) -> None:
        print("HELLO!!! and welcome to Quiplash!\n in this game you will receive an incomplete sentence. You must complete the sentence in the funniest way possible\nat the end all players will vote to the funniest sentence out of them all.")
