"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 07/04/24
    DESCRIPTION: This is the function that will be incharge of the game sequence.
"""
import random

from games import scene_one_explanation_of_game, round_one
from games.scene import Scene


def run_scene(scene_to_play: Scene):
    scene_to_play.scene()


def assign_sentences(sentences, players):
    """
    Randomly assigns sentences to players, ensuring each sentence has at most two players.
    :param sentences: Tuple of sentences (strings)
    :param players: List of Player objects
    :return: Dictionary with the sentence as the key and a tuple of usernames as the value
    """
    # Shuffle the list of players for randomness
    random.shuffle(players)

    # Prepare the result dictionary
    sentence_assignments = {sentence: [] for sentence in sentences}

    # List of usernames already assigned to a sentence
    assigned_usernames = set()

    # Create a list of indices for the sentences to shuffle
    sentence_indices = list(range(len(sentences)))
    random.shuffle(sentence_indices)

    # Assign players to sentences using shuffled indices
    player_iterator = iter(players)
    for index in sentence_indices:
        try:
            # Assign up to two players per sentence
            counter = 0
            while counter < 2:
                player = next(player_iterator)
                if player.username not in assigned_usernames:
                    sentence_assignments[sentences[index]].append(player)
                    assigned_usernames.add(player.username)
                    counter += 1
        except StopIteration:
            # No more players available
            break

    # Filter out any empty sentence assignments and convert lists to tuples
    final_assignments = {k: tuple(v) for k, v in sentence_assignments.items() if v}
    return final_assignments


def game_manager(players) -> None:
    """
    Handles the game sequence
    :param players: The player list
    :return: None
    """
    # Running the explanation of the game #
    run_scene(scene_one_explanation_of_game.Explanation())

    run_scene(round_one.RoundOne(players))
