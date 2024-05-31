"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 03/05/24
    DESCRIPTION: Waiting for players to join
"""
import socket

# Imports #
from quiplash.scene import Scene
from utils.global_vars import screen, text_font
from utils.functions import display_text
import quiplash.game_constants as consts
import utils.general_constants as global_consts

# items generation #
text_surface = text_font.render(f"Enter: {socket.gethostbyname(socket.gethostname())}:{global_consts.PORT}", True,
                                consts.COLOR_WHITE, None)
text_rect = text_surface.get_rect(
    center=(consts.WINDOW_WIDTH // 2, consts.WINDOW_HEIGHT // 2 + text_font.get_height() * 2), )


# Scene #
class WaitingLounge(Scene):
    """Waiting lounge - while waiting for players to join"""

    def __init__(self):
        """
        Constructor of class
        :return: None
        """
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
        display_text(screen,
                     "Wait for the other \t\t\tplayers",
                     (115, consts.WINDOW_HEIGHT // 2 - (text_font.get_height()) * 2),
                     text_font,
                     consts.COLOR_WHITE
                     )
        screen.blit(text_surface, text_rect)
