"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 07/04/24
    DESCRIPTION: This is the first round of the game.
"""
# Imports #
from quiplash.scene import Scene
from utils import global_vars
import quiplash.game_constants as consts
from utils.global_vars import screen, text_font
import random
import time

# Vars #
text_surface = text_font.render("Answer funny...", True, consts.COLOR_WHITE)
text_rect = text_surface.get_rect(center=(consts.WINDOW_WIDTH // 2, consts.WINDOW_HEIGHT // 2))


# Scene #
class PlayerSentences(Scene):
    """Sentence submission scene"""

    def __init__(self):
        """
        Constructor of class
        :return: None
        """

        # When instance of class is created the game_manager will already be locked by the game_main program #
        self.__PLAYERS = global_vars.game_manager.players

        self.__scene_over = False

        global_vars.round_start_time = time.time()

        # Set the sentence division of the players #
        global_vars.sentence_division = self.__assign_sentences(
            players=self.__PLAYERS, sentences=consts.GAME_PROMPTS)

        # Set submission counter to 0 - GAME_MANAGER IS ALREADY LOCKED #
        global_vars.game_manager.submission_counter = 0

    @property
    def scene_over(self) -> bool:
        """
        Is the scene over
        :return bool: Whether the scene is over or not
        """
        return self.__scene_over

    @staticmethod
    def __assign_sentences(sentences, players):
        """
        Randomly assigns sentences to players, ensuring each sentence has at most two players.
        :param sentences: Tuple of sentences (strings)
        :param players: List of Player objects
        :return: Dictionary with the sentence as the key and a tuple of usernames as the value
        """
        # Convert tuple to list
        sentences_list = list(sentences)

        # Make sure there are enough sentences for the players
        assert len(sentences_list) >= len(players) // 2, "Not enough sentences for all players."

        # Randomly shuffle the sentences and players
        random.shuffle(sentences_list)
        random.shuffle(players)

        # Create a dictionary to hold the sentence assignments
        assignments = {}

        # Pair up the players and assign them sentences
        for i in range(0, len(players), 2):
            sentence = sentences_list[i // 2]
            player1, player2 = players[i], players[i + 1]
            assignments[sentence] = [player1, player2]

        return assignments

    @staticmethod
    def __check_scene_over() -> bool:
        """
        Check if everyone submitted their sentence.
        CALL ONLY WHEN GAME MANAGER IS LOCKED!
        :return bool: Whether the scene is over or not. If Game_manager is locked will return False.
        """
        return_val = False

        # Game Manager is already locked when function is called.
        if global_vars.game_manager_lock.locked() and \
                global_vars.game_manager.submission_counter == consts.NUMBER_OF_PLAYERS_TO_START:
            return_val = True

        return return_val

    def scene(self) -> None:
        """
        The sentence scene
        :return: None
        """
        screen.blit(text_surface, text_rect)
        if self.__check_scene_over():
            self.__scene_over = True
