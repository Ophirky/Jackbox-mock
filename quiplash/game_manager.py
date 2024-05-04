"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 03/05/24
    DESCRIPTION: Handles the entire game
"""


class GameManager:
    """The game manager"""

    def __init__(self) -> None:
        """Constructor"""
        self.players = []
        self.game_started = False
        self.current_scene = 0

    def next_scene(self):
        """
        Goes to the next scene
        :return:
        """
        self.current_scene += 1
