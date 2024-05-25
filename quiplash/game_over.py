"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 26/05/2024
    DESCRIPTION: The game over scene. Shows scores.
"""
from quiplash.scene import Scene
from utils.global_vars import game_manager

class GameOver(Scene):
    """Game Over - When the game is over shows the final scores."""

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
        print("Game Over")
        for i in game_manager.players:
            print(f"{i.username} - {i.score}")
