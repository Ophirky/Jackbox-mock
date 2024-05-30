"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 03/05/24
    DESCRIPTION: Handles the server side front-end
"""
# Pygame import and setup
import pygame
import logging
import time

import quiplash.waiting_lounge as wait_lounge
from quiplash import player_sentences, voting_scene, game_over
from quiplash import game_constants as consts
from utils import global_vars

# Constants #
SCENE_ORDER = (wait_lounge.WaitingLounge, player_sentences.PlayerSentences,
               voting_scene.VotingScene, game_over.GameOver)

BG_GRADIENT_COLOR_ONE = pygame.Color("#f64f59")
BG_GRADIENT_COLOR_TWO = pygame.Color("#c471ed")
BG_GRADIENT_COLOR_THREE = pygame.Color("#12c2e9")

# variables init #
explanation_scene = None


def gradient_background() -> pygame.Surface:
    """
    This function creates the linear gradient for the background of the game.
    :return: None
    """
    gradient_surface = pygame.Surface((consts.WINDOW_WIDTH, consts.WINDOW_HEIGHT))

    # Create a 2x2 gradient bitmap
    gradient_bitmap = pygame.Surface((2, 2))
    pygame.draw.line(gradient_bitmap, BG_GRADIENT_COLOR_ONE, (0, 0), (0, 1))
    pygame.draw.line(gradient_bitmap, BG_GRADIENT_COLOR_TWO, (1, 0), (1, 1))
    pygame.draw.line(gradient_bitmap, BG_GRADIENT_COLOR_THREE, (2, 0), (1, 2))

    # Stretch the gradient to cover the entire window
    gradient_surface.blit(pygame.transform.smoothscale(gradient_bitmap, (consts.WINDOW_WIDTH, consts.WINDOW_HEIGHT)),
                          (0, 0))

    return gradient_surface


def run_scene(scene) -> None:
    """
    Executes a scene in the game
    :param scene: The scene to run
    :return: None
    """
    try:
        scene.scene()
    except TypeError as e:
        consts.LOGGER.error("Scene does not exist!")


def main() -> None:
    """
    The game's main program (scene handler)
    :return: None
    """
    # Setting up pygame #
    pygame.init()
    clock = pygame.time.Clock()

    pygame.display.set_caption("Quiplash")
    pygame.display.set_icon(pygame.image.load(consts.FAVICON_PATH))

    # Initializing the first scene #
    global_vars.current_scene_instance = SCENE_ORDER[global_vars.game_manager.current_scene]()
    running = True
    while running:
        # Thread delay #
        time.sleep(0.01)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                global_vars.app.close_app()
                pygame.quit()
                quit()

        # Draw background #
        global_vars.screen.blit(gradient_background(), (0, 0))

        # Lock game manager #
        with global_vars.game_manager_lock:
            # run the scene #
            run_scene(global_vars.current_scene_instance)

            # Move to scene #1 condition - game explanation #
            if (
                    (global_vars.game_manager.game_started and global_vars.game_manager.current_scene == 0)
                    or global_vars.current_scene_instance.scene_over
            ) and global_vars.game_manager.current_scene < len(SCENE_ORDER) - 1:
                logging.debug(global_vars.sentence_division)
                global_vars.game_manager.next_scene()
                global_vars.current_scene_instance = SCENE_ORDER[global_vars.game_manager.current_scene]()

        # Update the display
        pygame.display.flip()
        clock.tick(60)
