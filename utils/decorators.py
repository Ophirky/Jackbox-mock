"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 03/05/24
    DESCRIPTION: All the decorators for the project
"""
import logging

from utils.global_vars import game_manager_lock


def lock_game_manager(original_function):
    """
    Locking the game_manager for the entire function
    :param original_function: The original function
    :return: The original function return value
    """

    def wrapper_function(*args, **kwargs):
        """
        The wrapper function to the original function.
        :return: Original function return value
        """
        res = None
        with game_manager_lock:
            res = original_function(*args, **kwargs)
        return res

    return wrapper_function
