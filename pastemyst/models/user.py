from typing import Dict, Any, Optional, List

from pastemyst.utils.helpers import camel_to_snake, mangle_attr
from .language import Language


class User:
    """
    User class representing a user on pastemyst.

    The User class has the following methods:

    - id() -> str: Get the id of the user.
    - username() -> str: Get the username of the user.
    - avatar_url() -> str: Get the URL of the user's avatar image.
    - default_lang() -> Language: Get the default language for the user.
    - is_public_profile() -> bool: Returns True if the profile is public, False otherwise.
    - supporter_length() -> int: Get the length of time the user has been a supporter.
    - is_contributor() -> bool: Returns True if the user is a contributor to pastemyst, False otherwise.
    - stars() -> Optional[List[str]]: Get the list of paste ids the user has starred.
    - service_ids() -> Optional[Dict[str, str]]: Get the dictionary of service IDs for the user.
    - from_dict(data: Dict[str, Any]) -> User: Convert a dictionary representation of a user to a User object.
    """

    __slots__ = ("__id", "__username", "__avatar_url", "__default_lang", "__public_profile", "__supporter_length", "__contributor", "__stars", "__service_ids")

    @property
    def id(self) -> str:
        """
        Get the id of the user

        :return: The id of the user
        :rtype: str
        """
        return self.__id

    @property
    def username(self) -> str:
        """
        Get the username of the user

        :return: The username of the user
        :rtype: str
        """
        return self.__username

    @property
    def avatar_url(self) -> str:
        """
        Get the url of the user's avatar image

        :return: A string representing the avatar URL.
        :rtype: str
        """
        return self.__avatar_url

    @property
    def default_lang(self) -> Language:
        """
        Get the user's default language

        :return: The default language for the user
        :rtype: Language
        """
        return Language[self.__default_lang]

    @property
    def is_public_profile(self) -> bool:
        """
        Returns whether the profile is set as public or not.

        :return: True if the profile is public, False otherwise.
        :rtype: bool
        """
        return self.__public_profile

    @property
    def supporter_length(self) -> int:
        """
        Get how long has the user been a supporter for, 0 if not a supporter

        :return: The user's support length
        :rtype: int
        """
        return self.__supporter_length

    @property
    def is_contributor(self) -> bool:
        """
        Returns a boolean value indicating if the user is a contributor to pastemyst.

        :return: True if the user is a contributor, False otherwise.
        :rtype: bool
        """
        return self.__contributor

    @property
    def stars(self) -> Optional[List[str]]:
        """
        Get the list of paste ids the user has starred
        This only works if the user is yourself, retrieved by `Client.`

        :return: The ids of the users starred pastes as a list of strings, or None if there are no stars.
        :rtype: Optional[List[str]]
        """
        return getattr(self, mangle_attr(self, "__stars"), None)

    @property
    def service_ids(self) -> Optional[Dict[str, str]]:
        """
        Get the service IDs.

        :return: The dictionary with the service IDs, or None if not set.
        :rtype: Optional[Dict[str, str]]
        """
        return getattr(self, mangle_attr(self, "__service_ids"), None)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "User":
        """
        Convert a dictionary representation of a user to a User object.

        :param data: A dictionary containing user data.
        :type data: Dict[str, Any]
        :return: A User object.
        :rtype: User
        """
        user: User = User()
        for key, value in data.items():
            key = camel_to_snake(key)

            if key == "_id":
                key = "id"

            user.__setattr__(mangle_attr(user, f"__{key}"), value)

        return user
