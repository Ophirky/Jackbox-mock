"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 10/05/24
    DESCRIPTION: After everyone submitted their answers
"""
from quiplash.scene import Scene
from utils import global_vars
import quiplash.game_constants as consts


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

        if not self.__check_section_over():
            print(f"{current_sentence[0]}:\n {[player.answer for player in current_sentence[1]]}")
        else:
            player_one = current_sentence[1][0]
            player_two = current_sentence[1][1]

            player_one.add_score()
            player_two.add_score()

            winner = f"{player_one.username} and {player_two.username}"

            if player_one.voting_score > player_two.voting_score:
                winner = player_one.username
            elif player_one.voting_score < player_two.voting_score:
                winner = player_two.username

            global_vars.game_manager.current_sentence_vote += 1
            global_vars.game_manager.submission_counter = 0

            for player in global_vars.game_manager.players:
                player.voted = False

            print(f"winner: {winner}")

        with global_vars.sentence_division_lock:
            if len(global_vars.sentence_division) == global_vars.game_manager.current_sentence_vote:
                self.__scene_over = True
                global_vars.game_manager.game_over = True
