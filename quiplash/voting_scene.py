"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 10/05/24
    DESCRIPTION: After everyone submitted their answers
"""
import pygame

from quiplash.scene import Scene
from utils import global_vars, functions
import quiplash.game_constants as consts

# Define colors
glass_color = (180, 180, 180, 128)  # RGBA for a glass-like effect (semi-transparent)
box_color = (255, 255, 255, 128)  # Semi-transparent white color for the text boxes
text_color = (0, 0, 0)  # Black color for the text

# Load the font with a larger size for higher 'm'
font_size = 36  # Adjust the size as needed for a higher 'm'
answers_font = pygame.font.Font(consts.FONT_PATH, font_size)

# Calculate box dimensions
box_width = (consts.WINDOW_WIDTH // 2) - 20  # Two boxes with a 20-pixel gap in between
box_height = answers_font.get_height() * 8 + 40  # Increase the height for a taller 'm'

# Box positions
box1_pos = (10, consts.WINDOW_HEIGHT - box_height - 40)
box2_pos = (consts.WINDOW_WIDTH // 2 + 10, consts.WINDOW_HEIGHT - box_height - 40)

# Define border radius
border_radius = 15  # Adjust as needed for rounded corners


class VotingScene(Scene):
    """Voting scene"""

    def __init__(self):
        """Constructor"""
        self.__scene_over = False

        # Set submission counter to 0 - GAME_MANAGER IS ALREADY LOCKED #
        global_vars.game_manager.submission_counter = 0
        self.__start_ticks = pygame.time.get_ticks()
        self.__section_winner_shown = False

    @property
    def scene_over(self) -> bool:
        """
        Is the scene over
        :return bool: Whether the scene is over or not
        """
        return self.__scene_over

    @staticmethod
    def __check_section_over() -> bool:
        """
        Check if everyone submitted their game.
        :return bool: Whether the scene is over or not
        """
        return global_vars.game_manager.submission_counter == consts.NUMBER_OF_PLAYERS_TO_START

    def scene(self) -> None:
        """
        The waiting lounge (waiting for players) scene
        :return: None
        """
        current_sentence = None
        with global_vars.sentence_division_lock:
            current_sentence = list(global_vars.sentence_division.keys())[
                global_vars.game_manager.current_sentence_vote
            ], global_vars.sentence_division[
                list(global_vars.sentence_division.keys())[global_vars.game_manager.current_sentence_vote]
            ]
        # Voting scene #
        if not self.__check_section_over():
            functions.display_text(global_vars.screen, current_sentence[0] % "(blank)", (25, 75),
                                   answers_font, "white", right_padding=25)

            # Create the box surfaces with a border radius for the glass-like effect
            box_surface1 = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            pygame.draw.rect(box_surface1, box_color, (0, 0, box_width, box_height), border_radius=border_radius)
            box_surface2 = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            pygame.draw.rect(box_surface2, box_color, (0, 0, box_width, box_height), border_radius=border_radius)

            # Blit the box surfaces onto the screen
            functions.display_text(box_surface1, current_sentence[1][0].answer, (10, 10),
                                   answers_font, color="black", right_padding=10)
            functions.display_text(box_surface2, current_sentence[1][1].answer, (10, 10),
                                   answers_font, color="black", right_padding=10)
            global_vars.screen.blit(box_surface1, box1_pos)
            global_vars.screen.blit(box_surface2, box2_pos)

            # Set start ticks for 5 second text $
            self.__start_ticks = pygame.time.get_ticks()

        # Voting done scene - show section winner #
        elif not self.__section_winner_shown:
            player_one = current_sentence[1][0]
            player_two = current_sentence[1][1]

            player_one.add_score()
            player_two.add_score()

            global_vars.game_manager.current_sentence_vote += 1
            global_vars.game_manager.submission_counter = 0

            for player in global_vars.game_manager.players:
                player.voted = False

            else:
                self.__section_winner_shown = True

        with global_vars.sentence_division_lock:
            if len(global_vars.sentence_division) == global_vars.game_manager.current_sentence_vote:
                self.__scene_over = True
                global_vars.game_manager.game_over = True
