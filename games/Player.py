"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 06/04/24
    DESCRIPTION: This is the player class for the game.
"""

class Player:
    """Player class - contains the username and score of the player."""
    def __init__(self, username, is_admin=False) -> None:
        """
        Constructor of Player class
        :param username: The player username
        """
        self.username = username
        self.score = 0
        self.is_admin = is_admin

    def __str__(self):
        return f"{self.username}, {self.score}"

    def __eq__(self, other):
        if isinstance(other, str):
            return self.username == other
        elif isinstance(other, int):
            return self.score == other
        else:
            return self == other

