"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 07/04/24
    DESCRIPTION: This is the function that will be incharge of the game sequence.
"""
import random
from main import players

from games import scene_one_explanation_of_game, round_one
from games.scene import Scene
from usefull_files import general_constants as consts

def run_scene(scene_to_play: Scene):
    scene_to_play.scene()


def assign_sentences():

    if len(players) / 2 > len(consts.GAME_PROMPTS):
        raise ValueError("Not enough sentences for all players.")

    assignments = {}
    random.shuffle(players)

    print(len(players))

    for i in range(0, len(players), 2):
        sentence = consts.GAME_PROMPTS[i // 2]
        assignments[(players[i], players[i + 1])] = sentence

    return assignments


def game_manager():
    # Running the explanation of the game #
    run_scene(scene_one_explanation_of_game.Explanation())

    run_scene(round_one.RoundOne())
