"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 03/05/24
    DESCRIPTION: Waiting for players to join
"""
# Imports #
from quiplash.scene import Scene


# Scene #
class WaitingLounge(Scene):
    """Waiting lounge - while waiting for players to join"""
    def __init__(self):
        """Constructor"""
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
        The waiting lounge (waiting for players) scene
        :return: None
        """
        print("Wait for everyone to enter")
