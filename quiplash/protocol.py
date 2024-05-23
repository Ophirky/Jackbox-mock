"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 05/11/24
    DESCRIPTION: This file will handle the protocol of the game.
"""
import json
from quiplash import game_constants as consts

class QuiplashProtocol:
    """Protocol Functions - format and deformat"""

    @staticmethod
    def format(time_left: float = None, txt: str = None, start_game: bool = None) -> bytes:
        """
        This will take the params given in the arguments.
        :param time_left: The time left for a round.
        :param txt: Any kind of text that needs to be transmitted between the client and the server..
        :param start_game: Whether the game started or not.
        :return str: Returns a string formatted by the protocol.
        """
        formatted_protocol: dict[str] = dict()
        if time_left:
            formatted_protocol["time-left"] = str(time_left)
        if txt:
            formatted_protocol["txt"] = txt
        if start_game:
            formatted_protocol["start-game"] = str(start_game)

        return json.dumps(formatted_protocol).encode()

    @staticmethod
    def deformat(msg: str) -> dict:
        """
        Returns a dict with the protocol.
        :param msg: The msg to be deformatted
        :return dict(str): The dict in the protocol format if the message is not json it will return an empty dict.
        """
        res = dict()
        try:
            res = json.loads(msg)
        except json.JSONDecodeError or json.decoder.JSONDecodeError:
            consts.LOGGER.exception("The message is not in json format")

        return res

def protocol_auto_tests() -> None:
    """
    Auto tests for the file.
    :return: None
    """
    protocol = QuiplashProtocol()

    # Test formatting
    formatted_msg = protocol.format(time_left=30.0, txt="Hello, world!", start_game=True)
    assert isinstance(formatted_msg, bytes), "Formatted message should be of type 'bytes'"

    # Test deformatting (valid JSON)
    valid_msg = '{"time-left": "30.0", "txt": "Hello, world!", "start-game": "true"}'
    deformatted_dict = protocol.deformat(valid_msg)
    assert isinstance(deformatted_dict, dict), "Deformatted message should be a dictionary"
    assert deformatted_dict["time-left"] == "30.0", "Incorrect 'time-left' value"
    assert deformatted_dict["txt"] == "Hello, world!", "Incorrect 'txt' value"
    assert deformatted_dict["start-game"] == "true", "Incorrect 'start-game' value"
