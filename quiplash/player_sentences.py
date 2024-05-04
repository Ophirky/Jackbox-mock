"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 07/04/24
    DESCRIPTION: This is the first round of the game.
"""
# Imports #
from quiplash.scene import Scene
from quiplash import game_constants as consts
from utils import global_vars
import random
import time


# Scene #
class PlayerSentences(Scene):
    """Round One"""

    def __init__(self):
        """Constructor of Round One"""

        # When instance of class is created the game_manager will already be locked by the game_main program #
        self.__PLAYERS = global_vars.game_manager.players

        self.__scene_over = False

        global_vars.round_start_time = time.time()

        # Set the sentence division of the players #
        # with global_vars.sentence_division_lock:
        global_vars.sentence_division = self.__assign_sentences(
            players=self.__PLAYERS, sentences=consts.GAME_PROMPTS)

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
        print(sentences)
        print(str(player) + ", " for player in players)
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

    def scene(self) -> None:
        """
        The sentence scene
        :return: None
        """
        # print("Alright! let's get it started!")
        self.__scene_over = True
