from datetime import datetime, timezone
from typing import Dict, Any, List

import trio

from pastemyst.utils import mangle_attr
from pastemyst.models import RequestError, ExpiresIn, User, LanguageInfo, Paste, HttpError, PasteResult
from pastemyst.api.http import HttpClient


class Client:
    """
    Client class for interacting with the pastemyst API.
    """

    __slots__ = ("key", "is_dev", "api")

    def __init__(self, key: str = None, is_dev: bool = False):
        self.key = key
        self.is_dev = is_dev

        self.api = HttpClient(key, is_dev)

    def authenticate(self, key: str) -> None:
        """
        Authenticates the client with the provided key.

        :param key: The API key for the user.
        :type key: str
        :return: None
        """
        self.key = key
        self.api.auth(key)

    @property
    def is_authenticated(self) -> bool:
        """
        Check if the client is authenticated.

        :return: True if the client is authenticated, False otherwise.
        :rtype bool
        """
        return self.api.is_authenticated

    def get_language_info(self, *, name: str = None, extension: str = None) -> LanguageInfo:
        """
        Retrieve information about a programming language based on its name or file extension.

        :param name: The name of the programming language.
        :type name: str
        :param extension: The file extension of the programming language.
        :type extension: str
        :return: An instance of LanguageInfo containing information about the programming language.
        :rtype: LanguageInfo
        """
        result: Dict[str, Any] = trio.run(self.api.get_language, name, extension)
        return LanguageInfo.from_dict(result)

    def paste_exists(self, paste_id: str) -> bool:
        """
        Check if a paste exists.

        :param paste_id: The ID of the paste to check.
        :type paste_id: str
        :return: True if the paste exists, False otherwise.
        :rtype: bool
        """
        if paste_id is None or paste_id == "":
            return False

        try:
            _: Dict[str, Any] = trio.run(self.api.get_paste, paste_id)
            return True
        except HttpError as e:
            if e.status_code == 404:
                return False
            else:
                raise e

    def get_paste(self, paste_id: str) -> PasteResult:
        """
        Retrieves a paste with the given paste_id.

        :param paste_id: The ID of the paste to retrieve.
        :type paste_id: str
        :return: The PasteResult object representing the retrieved paste.
        :rtype: PasteResult
        """
        result: Dict[str, Any] = trio.run(self.api.get_paste, paste_id)
        return PasteResult.from_dict(result)

    def create_paste(self, paste: Paste) -> PasteResult:
        """
        Create a paste object.

        :param paste: The paste object to be created.
        :type paste: Paste
        :return: The result of the paste creation.
        :rtype: PasteResult
        :raises RequestError: If the paste object has no pasties.
        """
        if len(paste.pasties) < 1:
            raise RequestError("paste object must have at least one pasty")

        result: Dict[str, Any] = trio.run(self.api.create_paste, paste)
        return PasteResult.from_dict(result)

    def edit_paste(self, paste: Paste, target_id: str = None) -> PasteResult:
        """
        Updates / edits the given paste. The paste must have already been uploaded, and either contain a paste ID or a target ID must be provided

        :param paste: The Paste object to be edited.
        :type paste: Paste
        :param target_id: The ID of the target paste to edit. If None, the ID of the provided Paste object will be used as the target ID.
        :type target_id: str
        :return: A PasteResult object containing the result of the paste edit operation.
        :rtype: PasteResult
        """
        result: Dict[str, Any] = trio.run(self.api.edit_paste, paste, target_id or getattr(paste, mangle_attr(Paste, "__id"), None))
        return PasteResult.from_dict(result)

    def delete_paste(self, paste: str | PasteResult) -> bool:
        """
        Deletes a paste.
        You must be authenticated to perform this, and you can only perform it if the paste belongs to you

        :param paste: The paste to delete. It can be either a string representing the paste ID or a PasteResult object.
        :type paste: str | PasteResult
        :return: True if the paste was successfully deleted, False otherwise.
        :rtype: bool
        :raises RequestError: If the user is not authenticated or if the paste does not have an id field.
        """
        if not self.is_authenticated:
            raise RequestError("you must be authenticated before deleting your own paste")

        if isinstance(paste, PasteResult):
            if not hasattr(paste, "id"):
                raise RequestError("paste must have id field")

            paste_id = paste.id
        else:
            paste_id = paste
        result: int = trio.run(self.api.delete_paste, paste_id)
        return result == 200

    def get_expire_stamp(self, paste: str | PasteResult) -> datetime:
        """
        This method retrieves the expiration stamp of a given paste. The `paste` parameter can be either a string representing the ID of the paste or a `PasteResult` object containing details
        * about the paste.

        If the `paste` parameter is a string, it is first converted to a `PasteResult` object by calling the `get_paste` method of the current instance.

        The method checks if the paste has the required fields `expires_in` and `created_at`. If any of these fields is missing, a `RequestError` is raised.

        If the `expires_in` field is set to `ExpiresIn.NEVER`, indicating that the paste never expires, a `RequestError` is raised as it is not possible to determine the expiration stamp of
        * a paste that never expires.

        The method calculates the UNIX timestamp of the paste's creation time by subtracting the UNIX timestamp of January 1, 1970 from the paste's `created_at` timestamp and converting it to
        * seconds. The resulting value is assigned to the `unix_stamp` variable.

        The method then calls the `get_expire_unix` method of the `api` object (assuming it is an instance of a class with an `api` attribute) with the `unix_stamp` and `expires_in` values as
        * arguments. The returned value is assigned to the `result` variable.

        Finally, the method converts the `result` value to an integer and passes it along with the `timezone.utc` argument to the `fromtimestamp` method of the `datetime` module. The resulting
        * `datetime` object representing the expiration stamp is returned.

        :param paste: Either a string representing the ID of the paste or a `PasteResult` object.
        :type paste: str | PasteResult
        :return: A `datetime` object representing the expiration stamp of the paste.
        :rtype: datetime
        """
        if isinstance(paste, str):
            paste = self.get_paste(paste)

        if not paste.expires_in:
            raise RequestError("paste must have expires_in field")
        if not paste.created_at:
            raise RequestError("paste must have created_at field")
        if paste.expires_in == ExpiresIn.NEVER:
            raise RequestError("can't find expiration stamp of paste that never expires")

        unix_stamp: float = (datetime.fromtimestamp(paste.created_at.timestamp()) - datetime(1970, 1, 1)).total_seconds()
        result: int = trio.run(self.api.get_expire_unix, int(unix_stamp), paste.expires_in.value)
        return datetime.fromtimestamp(int(result), timezone.utc)

    def user_exists(self, username: str) -> bool:
        """
        Checks if a user with the given username exists

        :param username: The username to check if it exists.
        :type username: str
        :return: True if the user exists, False otherwise.
        :rtype: bool
        """
        result: int = trio.run(self.api.get_user_exists, username)
        return result == 200

    def get_user(self, username: str) -> User:
        """
        Gets a user with the given username

        :param username: The username of the user to retrieve
        :type username: str
        :return: A User object representing the retrieved user information
        :rtype: User
        """
        result: Dict[str, Any] = trio.run(self.api.get_user, username)
        return User.from_dict(result)

    def get_self_user(self) -> User:
        """
        Get information about the authenticated user.

        :return: The user information as an instance of the User class.
        :rtype: User
        """
        result: Dict[str, Any] = trio.run(self.api.get_self)
        return User.from_dict(result)

    def get_self_user_pastes(self) -> List[PasteResult]:
        """
        Retrieves all the pastes created by the authenticated user.

        :return: A list of PasteResult objects representing the pastes created by the self user.
        :rtype: List[PasteResult]
        """
        result: List[str] = trio.run(self.api.get_self_pastes)
        pastes: List[PasteResult] = []
        for paste in result:
            pastes.append(self.get_paste(paste))
        return pastes
