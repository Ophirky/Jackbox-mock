"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 15/03/24
    DESCRIPTION: Takes a received http request and formats it into a structure that is easy to use in code
"""
# Imports #
import http.constants as consts
import http


# HttpParser #
class HttpParser:
    """Class to make http request usable in code more easily"""
    def __init__(self, http_request: bytes) -> None:
        """
        The constructor of the HttpParser class.
        :param http_request: the request for the class to parse.
        """
        # If the request is invalid #
        is_request_valid = http.is_valid_request(http_request)
        if not is_request_valid["valid"]:
            self.HTTP_REQUEST = is_request_valid["reason"]
            self.QUERY_PARAMS = None
            self.HEADERS = None
            self.BODY = None

        # If the request is valid #
        else:
            self.HTTP_REQUEST = http_request

            self.QUERY_PARAMS = self.__query_params_parser()
            self.HEADERS = self.__header_parser()
            self.BODY = self.__body_parser()

        # Whether the request is valid #
        self.IS_VALID: bool = is_request_valid["valid"]

    def __header_parser(self) -> dict[bytes]:
        """
        Extracts the headers from the request
        :return dict[bytes]: {header: value}
        """
        return dict(x.split(b": ") for x in self.HTTP_REQUEST.split(consts.HEADER_SEPERATOR)[1:-2])

    def __body_parser(self) -> bytes:
        """
        Extracts the body from the requests
        :return bytes: the body of the request
        """
        return self.HTTP_REQUEST.split(consts.BODY_SEPERATOR)[1]

    def __query_params_parser(self) -> dict[bytes] or None:
        """
        Extract the parameters from the http request
        :return: dictionary of all the query parameters
        """
        try:
            return dict(
                x.split(b" ")[0].split(b"=", 1)[0:2] for x in self.HTTP_REQUEST.split(b"?", 1)[1].split(b"&", 1))

        # If there are no params #
        except IndexError:
            return None


def auto_test_http_parser() -> None:
    """
    Automatic tests for the HttpParser class.
    :return: None
    """
    # Valid HTTP request with query parameters
    valid_request = b"GET /index.html?param1=value1&param2=value2 HTTP/1.1\r\nHost: example.com\r\n\r\n"
    parser_valid = HttpParser(valid_request)
    assert parser_valid.IS_VALID
    assert parser_valid.HTTP_REQUEST == valid_request
    assert parser_valid.QUERY_PARAMS == {b"param1": b"value1", b"param2": b"value2"}
    assert parser_valid.HEADERS == {b"Host": b"example.com"}
    assert parser_valid.BODY == b""

    # Invalid HTTP request
    parser_invalid = HttpParser(b"GET /index.html HTTP/1.1\r\nHost: example.com\r\nInvalid-Header\r\n\r\n")
    assert not parser_invalid.IS_VALID
    assert not parser_invalid.QUERY_PARAMS
    assert not parser_invalid.HEADERS
    assert not parser_invalid.BODY
