from typing import Dict, Any
from httpx import Response


class PastemystError(Exception):
    """
    Represents an error that occurred within the Pastemyst API.

    This class inherits from the built-in Exception class and is used to raise custom errors specific to the Pastemyst API.
    """
    pass


class HttpError(PastemystError):
    """
    Represents an HTTP error with detailed information about the request and response.

    :param response: The HTTP response object.
    :type response: Response
    :param data: The error data, which can be a dictionary or a string.
    :type data: Dict[str, Any] or str
    """
    __slots__ = ("response", "status_code", "reason", "method", "message")

    def __init__(self, response: Response, data: Dict[str, Any] | str):
        self.status_code = response.status_code
        self.reason = response.reason_phrase
        self.method = response.request.method
        self.url = response.request.url

        if isinstance(data, dict):
            self.message = data.get("statusMessage", "")
        else:
            self.message = str(data)

        super().__init__("{0.status_code} {0.reason} ({0.method} {0.url}): {0.message}".format(self))


class RequestError(PastemystError):
    """
    A custom exception class to represent an error occurred while making a request.

    Inherits from PastemystError.
    """
    pass
