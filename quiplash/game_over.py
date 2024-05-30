"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 26/05/2024
    DESCRIPTION: The game over scene. Shows scores.
"""
from quiplash.scene import Scene
from utils.global_vars import game_manager
import quiplash.game_constants as consts
from utils.global_vars import text_font, screen

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
        winners = [game_manager.players[0]]
        for i in game_manager.players[1:]:
            if winners[0].score > i.score:
                winners = [i]
            elif winners[0].score == i.score:
                winners.append(i)

        if len(winners) == 1:
            text_surface = text_font.render(f"The winner is {winners[0].username}", True, consts.COLOR_WHITE, None)
            text_rect = text_surface.get_rect(center=(consts.WINDOW_WIDTH // 2, consts.WINDOW_HEIGHT // 2), )
            screen.blit(text_surface, text_rect)
        else:
            current_letter_y = consts.WINDOW_HEIGHT // 2 - (len(winners)+1 * text_font.get_height())
            text_surface = text_font.render(f"The winners are", True, consts.COLOR_WHITE, None)
            text_rect = text_surface.get_rect(center=(consts.WINDOW_WIDTH // 2, current_letter_y))
            screen.blit(text_surface, text_rect)
            for i in range(0, len(winners)):
                current_letter_y += text_font.get_height()
                text_surface = text_font.render(winners[i].username, True, consts.COLOR_WHITE, None)
                text_rect = text_surface.get_rect(center=(consts.WINDOW_WIDTH // 2, current_letter_y), )
                screen.blit(text_surface, text_rect)
