"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 10/05/24
    DESCRIPTION: After everyone submitted their answers
"""
from quiplash.scene import Scene


class VotingScene(Scene):
    """Voting scene"""
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
        print("Voting for a sentence")
