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
        self.submission_counter = 0
        self.current_sentence_vote = 0
        self.game_over = False

    def next_scene(self):
        """
        Goes to the next scene
        :return:
        """
        self.current_scene += 1

def game_manager_auto_asserts() -> None:
    """
    Auto tests of this file
    :return: None
    """
    test_game_manager = GameManager()
    assert isinstance(test_game_manager, GameManager)
    assert test_game_manager.current_scene == 0
    test_game_manager.next_scene()
    assert test_game_manager.current_scene == 1
