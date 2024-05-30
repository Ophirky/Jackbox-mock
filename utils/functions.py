"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 29/05/2024
    DESCRIPTION: Holds all needed functions for game.
"""
import threading
import pygame
from utils import global_vars
import quiplash.game_constants as gconsts


def display_text(surface: pygame.Surface, text: str, pos: tuple, font: pygame.font.Font, color: str,
                 right_padding: int = 0) -> None:
    """
    Will print text to the pygame surface given
    :param right_padding: Allow adding padding on the right
    :param surface: The surface to add the text to.
    :param text: The text to add
    :param pos: The position of the text on the surface
    :param font: The font for the text
    :param color: The color for the text
    :return: None
    """
    # Get the different lines in the text 3
    collection = [word.split(' ') for word in text.splitlines()]

    space = font.size(' ')[0]  # letter height

    x, y = pos
    word_height = None  # Initializing the word height

    for lines in collection:
        for words in lines:
            word_surface = font.render(words, True, color, None)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= gconsts.WINDOW_WIDTH-right_padding:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]

        try:
            y += word_height
        except TypeError:
            gconsts.LOGGER.exception("Added word height while not defined.")


def close_socket_thread() -> None:
    """
    Closes the socket thread.
    :return: None
    """
    if isinstance(global_vars.socket_thread, threading.Thread) and global_vars.socket_thread.is_alive():
        threading.Event().set()
        global_vars.socket_thread.join()
