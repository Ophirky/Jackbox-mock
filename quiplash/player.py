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
        :return: None
        """
        self.username = username
        self.score = 0
        self.is_admin = is_admin
        self.answer = None
        self.voted = False
        self.voting_score = 0

    def add_score(self) -> None:
        """
        Add 1000 points to the player's score.
        :return: None
        """
        self.score += 1000 * self.voting_score

    def __str__(self):
        """
        When class is cast to string.
        :return: String including the username and current score
        """
        return f"{self.username}, {self.score}"