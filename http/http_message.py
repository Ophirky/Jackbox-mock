"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 15/03/24
    DESCRIPTION: Class that allows to create easy to use http messages including responses and requests
"""
# Imports #
import http.constants as consts

class HttpMsg:
    """create easy to use http messages including responses and requests"""
    def __init__(self, error_code: int = 200, body=b"", **headers) -> None:
        self.error_code = self.__error_code_finder(error_code)
        self.body = body
        self.headers = headers

    def __error_code_finder(self, error_code: int):
        """
        returns the error code and messge using the error code.
        :param error_code: the error code to be found
        :return: str the error code
        """
        if error_code in ERROR_CODES.keys():
            return str(error_code).encode() + b" " + ERROR_CODES[error_code]
        else:
            return "-1"