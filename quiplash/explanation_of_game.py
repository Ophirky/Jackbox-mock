"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 07/04/24
    DESCRIPTION: This is the first scene of the game. once it is started.
"""
# Imports #
from quiplash.scene import Scene
from utils import general_constants as consts


# Scene #
class Explanation(Scene):
    """The explanation of the game"""
    def __init__(self):
        """The class constructor"""
        self.__scene_over = False

    @property
    def scene_over(self) -> bool:
        """
        Is the scene over
        :return bool: Whether the scene is over or not
        """
        return self.__scene_over

    def scene(self) -> None:
        """
        The explanation scene
        :return: None
        """
        print("HELLO!!! and welcome to Quiplash!\n in this game you will receive an incomplete sentence. You must complete the sentence in the funniest way possible\nat the end all players will vote to the funniest sentence out of them all.")
        self.__scene_over = True


