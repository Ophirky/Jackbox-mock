"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 10/05/24
    DESCRIPTION: After everyone submitted their answers
"""
from quiplash.scene import Scene
from utils import global_vars
import quiplash.game_constants as consts
import logging

class VotingScene(Scene):
    """Voting scene"""

    def __init__(self):
        """Constructor"""
        self.__scene_over = False

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
    def __check_section_over() -> bool:
        """
        Check if everyone submitted their game.
        :return bool: Whether the scene is over or not
        """
        return_val = False

        if global_vars.game_manager.submission_counter == consts.NUMBER_OF_PLAYERS_TO_START:
            return_val = True

        return return_val

    def scene(self) -> None:
        """
        The waiting lounge (waiting for players) scene
        :return: None
        """
        for sentence, players in global_vars.sentence_division.items():
            global_vars.game_manager.current_sentence_vote = (sentence, players)
            while not self.__check_section_over():
                print(f"{sentence}:\n {[player.answer for player in players]}")

            global_vars.game_manager.current_sentence_vote = 0

        self.__scene_over = True
