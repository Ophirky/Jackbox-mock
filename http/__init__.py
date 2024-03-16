"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 15/03/24
    DESCRIPTION: HTTP protocol package. Includes (http parser and formatter, http request builder)
"""

import constants as consts

def is_valid_request(request):
    """
    Checks if a http request is valid.
    :param request: the request to validate.
    :return dict[bool, string]: {"valid": True/False, "reason":"reason"}
    """

    # Split the request into lines #
    lines = request.split('\r\n')

    # Check if there's at least one line (the request line) and a blank line separating headers and body #
    if len(lines) < 2 or '\r\n\r\n' not in request:
        return {"valid": False, "reason": "At least one line (the request line) and a blank line separating headers "
                                          "and body are needed."}

    # Check the request line for the correct number of elements and separators #
    request_line_parts = lines[0].split(' ')
    if len(request_line_parts) < 3:
        return {"valid": False, "reason": "Incorrect number of elements or separators."}

    # Ensure method, path, and HTTP version are correctly separated #
    method, path, version = request_line_parts[0], request_line_parts[1], request_line_parts[-1]
    if method.encode() not in consts.REQUEST_TYPES.values():
        return {"valid": False, "reason": f"{method} is not a real method in http."}

    # Check if the request has an http version #
    if not method or not path or not version.startswith('HTTP/'):
        return {"valid": False, "reason": "Request must have http version."}


    # Check headers for correct formatting
    is_host_header = False
    for header in lines[1:-2]:  # Ignoring the request line and the last two elements (the last header and the body)
        if ': ' not in header:
            return {"valid": False, "reason": f"{header} header does not contain colon-space separator."}
        if "Host" in header:
            is_host_header = True # Mandatory host header is in the request

    # Check if the request has mandatory host header #
    if not is_host_header:
        return {"valid": False, "reason": "Host header is mandatory."}

    # Return true if the request is valid #
    return {"valid": True}
