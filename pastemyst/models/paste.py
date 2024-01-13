from datetime import datetime, timezone
from enum import Enum, IntEnum
from typing import Dict, Any, List, TypeVar, Optional

from pastemyst.models.language import Language
from pastemyst.models.errors import PastemystError
from pastemyst.utils.helpers import camel_to_snake, mangle_attr


T = TypeVar("T", bound="JsonObject")


class ExpiresIn(str, Enum):
    """
    Represents the expiration time for a paste.

    :param str ONE_HOUR: Represents an expiration time of 1 hour.
    :param str TWO_HOURS: Represents an expiration time of 2 hours.
    :param str TEN_HOURS: Represents an expiration time of 10 hours.
    :param str ONE_DAY: Represents an expiration time of 1 day.
    :param str TWO_DAYS: Represents an expiration time of 2 days.
    :param str ONE_WEEK: Represents an expiration time of 1 week.
    :param str ONE_MONTH: Represents an expiration time of 1 month.
    :param str ONE_YEAR: Represents an expiration time of 1 year.
    :param str NEVER: Represents an expiration time that never expires.
    """

    ONE_HOUR:   str = "1h"
    TWO_HOURS:  str = "2h"
    TEN_HOURS:  str = "10h"
    ONE_DAY:    str = "1d"
    TWO_DAYS:   str = "2d"
    ONE_WEEK:   str = "1w"
    ONE_MONTH:  str = "1m"
    ONE_YEAR:   str = "1y"
    NEVER:      str = "never"


class EditType(IntEnum):
    """
    An enumeration representing the type of edit made to a paste.

    Attributes:
        TITLE: int
            Represents an edit made to the title of the paste.
        PASTY_TITLE: int
            Represents an edit made to the title of a pasty.
        PASTY_LANGUAGE: int
            Represents an edit made to the language of a pasty.
        PASTY_CONTENT: int
            Represents an edit made to the content of a pasty.
        PASTY_ADDED: int
            Represents an addition of a pasty to a paste.
        PASTY_REMOVED: int
            Represents a removal of a pasty from a paste.
    """

    TITLE:          int = 0
    PASTY_TITLE:    int = 1
    PASTY_LANGUAGE: int = 2
    PASTY_CONTENT:  int = 3
    PASTY_ADDED:    int = 4
    PASTY_REMOVED:  int = 5


class Pasty:
    """
    A class representing a code snippet / pasty.

    Methods:
        __init__(self, title: str = "untitled", code: str = "", language: Language = Language.AUTODETECT)
            Initializes a new Pasty object with the given title, code and language.

        id() -> Optional[str]:
            Returns the unique identifier of the pasty.

        title() -> str:
            Returns the title of the pasty.

        code() -> str:
            Returns the code content of the pasty.

        language() -> Language:
            Returns the language of the code.

        from_dict(data: Dict[str, Any]) -> Pasty:
            Creates a Pasty object from a dictionary representation.

        to_dict() -> Dict[str, Any]:
            Converts the Pasty object to a dictionary representation.

    """
    __slots__ = ("__id", "__title", "__code", "__language")

    def __init__(self, title: str = "untitled", code: str = "", language: Language = Language.AUTODETECT):
        self.__title = title
        self.__code = code
        self.__language = language

    @property
    def id(self) -> Optional[str]:
        """
        Returns the ID of the pasty.

        :return: The ID of the object if available, or None if not set.
        :rtype: Optional[str]
        """
        return getattr(self, mangle_attr(self, "__id"), None)

    @property
    def title(self) -> str:
        """
        Return the title of the pasty.

        :return: The title of the pasty.
        :rtype: str
        """
        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        """
        Set the value of the title attribute.

        :param value: The value to set for the title.
        :type value: str
        :return: None
        """
        self.__title = str(value)

    @property
    def code(self) -> str:
        """
        Return the code associated with this pasty.

        :return: The code as a string.
        :rtype: str
        """
        return self.__code

    @code.setter
    def code(self, value: str) -> None:
        """
        Setter method for the code attribute.

        :param value: The new value for the code attribute.
        :type value: str
        :return: None
        """
        self.__code = str(value)

    @property
    def language(self) -> Language:
        """
        :return: The programming language of the method.
        :rtype: Language
        """
        return self.__language

    @language.setter
    def language(self, value: Language) -> None:
        """
        This method sets the language of the pasty to the provided `value`. If `value` is not an instance of `Language`, it will be converted to an instance of `Language`.

        :param value: The language to be set for the object.
        :return: None.
        """
        if not isinstance(value, Language):
            value = Language(value)
        self.__language = value

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Pasty":
        """
        Create a `Pasty` instance from a dictionary.

        :param data: A dictionary containing the data for the `Pasty` instance.
        :type data: Dict[str, Any]
        :return: An instance of the `Pasty` class.
        :rtype: Pasty
        """
        pasty: Pasty = Pasty()
        for key, value in data.items():
            key = camel_to_snake(key)

            if key == "_id":
                key = "id"
            elif key == "language":
                value = Language(value)

            pasty.__setattr__(mangle_attr(pasty, f"__{key}"), value)

        return pasty

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dictionary.

        :return: The converted dictionary.
        :rtype: Dict[str, Any]
        """
        data: Dict[str, Any] = {
            "language": self.language.value if isinstance(self.language, Language) else self.language,
            "title": self.title,
            "code": self.code
        }

        if self.id is not None:
            data["_id"] = self.id

        return data


class PasteEdit:
    """

    A class representing an edit made to a paste. It contains information such as the ID of the edit, the type of edit, the edited content, and the timestamp of when the edit was
    * made.

    Properties:
        id (str): The ID of the paste edit.
        edit_id (str): The ID of the paste being edited.
        edit_type (EditType): The type of edit made.
        metadata (List[str]): A list of metadata associated with the edit.
        edit (str): The edited content.
        edited_at (datetime): The timestamp of when the edit was made.

    Methods:
        from_dict(data: Dict[str, Any]) -> "PasteEdit":
            Creates a `PasteEdit` instance using the provided dictionary of data.

    """
    __slots__ = ("__id", "__edit_id", "__edit_type", "__metadata", "__edit", "__edited_at")

    @property
    def id(self) -> str:
        """Returns the ID of the paste.

        :return: The ID of the paste.
        :rtype: str
        """
        return self.__id

    @property
    def edit_id(self) -> str:
        """
        Returns the edit ID.

        :return: The edit ID as a string.
        :rtype: str
        """
        return self.__edit_id

    @property
    def edit_type(self) -> EditType:
        """
        Returns the edit type of the edit.

        :return: The edit type of the edit.
        :rtype: EditType
        """
        return self.__edit_type

    @property
    def metadata(self) -> List[str]:
        """
        Various metadata used internally by pastemyst.
        Biggest use case is storing exactly which pasty was edited

        :return: The metadata as a list of strings.
        :rtype: List[str]
        """
        return self.__metadata

    @property
    def edit(self) -> str:
        """
        Actual paste edit, it stores old data before the edit as the current paste stores the new data

        :return: The old paste data.
        :rtype: str
        """
        return self.__edit

    @property
    def edited_at(self) -> datetime:
        """
        Return the datetime when the edit happened.

        :return: The datetime of the edit.
        :rtype: datetime.datetime
        """
        return self.__edited_at

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "PasteEdit":
        """
        Creates a PasteEdit object from a dictionary.

        :param data: The dictionary containing the PasteEdit data.
        :type data: Dict[str, Any]
        :return: The created PasteEdit object.
        :rtype: PasteEdit
        """
        paste_edit: PasteEdit = PasteEdit()
        for key, value in data.items():
            key = camel_to_snake(key)

            if key == "_id":
                key = "id"
            elif key == "edited_at":
                value = datetime.fromtimestamp(int(value), timezone.utc)
            elif key == "edit_type":
                value = EditType(value)

            paste_edit.__setattr__(mangle_attr(paste_edit, f"__{key}"), value)

        return paste_edit


class Paste:
    """
    The `Paste` class represents a paste which contains a collection of `Pasty` objects. It provides methods for accessing and manipulating the properties of the paste.
    It is used when creating new paste's
    """

    __slots__ = ("__title", "__pasties", "__expires_in", "__is_private", "__is_public", "__tags")

    def __init__(self, title: str = "untitled", pasties: List[Pasty] = None, expires_in: ExpiresIn = ExpiresIn.ONE_HOUR, is_private: bool = False, is_public: bool = False, tags: List[str] = None):
        self.__title = title
        self.__pasties = pasties if pasties else []
        self.__expires_in = expires_in
        self.__is_private = is_private
        self.__is_public = is_public
        self.__tags = tags if tags else []

    @property
    def title(self) -> str:
        """
        Get the title of the paste.

        :return: The title as a string.
        :rtype: str
        """
        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        """
        Sets the title of the paste

        :param value: The new title of the method. It must be a string.
        :return: None
        """
        self.__title = str(value)

    @property
    def pasties(self) -> List[Pasty]:
        """
        Get the pasties of the paste.

        :return: A list of Pasty objects.
        :rtype: List[Pasty]
        """
        return self.__pasties

    def add_pasty(self, pasty: Pasty) -> None:
        """
        This method takes a Pasty object as a parameter and adds it to the paste's pasties. If the Pasty object already has an id assigned, the
        id attribute is set to None before adding it to the list.

        :param pasty: The Pasty object to be added to the list of pasties.
        :type pasty: Pasty
        :return: None
        """
        if pasty.id is not None:
            pasty.__setattr__(mangle_attr(pasty, "__id"), None)
        self.__pasties.append(pasty)

    def remove_pasty(self, pasty: Pasty | str | int) -> None:
        """
        Removes the given pasty object or identifier from the list of pasties.
        If the pasty parameter is an instance of the Pasty class, it is directly removed from the list.
        If the pasty parameter is a string, it is treated as an identifier and the corresponding Pasty object is retrieved using the `get_pasty_by_id` or `get_pasty_by_name` methods. If a matching
        * Pasty object is found, it is removed from the list.
        If the pasty parameter is an integer, it is treated as an index and the Pasty object at that index is removed from the list.

        Note:
        - If the pasty parameter is an integer and the index is out of range, no action is taken.
        - If multiple Pasty objects have the same identifier or name, only the first one found will be removed.

        :param pasty: The pasty object or identifier to be removed from the list of pasties.
        :type pasty: Pasty | str | int
        :return: None
        """
        if isinstance(pasty, Pasty):
            self.__pasties.remove(pasty)
        elif isinstance(pasty, str):
            pst: Pasty = self.get_pasty_by_id(pasty) or self.get_pasty_by_name(pasty) or None
            if pst is not None:
                self.__pasties.remove(pst)
        elif isinstance(pasty, int):
            if 0 <= pasty < len(self.__pasties):
                self.__pasties.pop(pasty)

    def get_pasty(self, index: int) -> Optional[Pasty]:
        """
        Gets a pasty from the paste by its index in the list

        :param index: An integer representing the index of the pasty to retrieve.
        :type index: int
        :return: The Pasty object at the specified index, or None if the index is out of range.
        :rtype: Optional[Pasty]
        """
        return self.__pasties[index] if 0 <= index < len(self.__pasties) else None

    def get_pasty_by_id(self, id: str) -> Optional[Pasty]:
        """
        Finds a Pasty in the collection by its ID.

        :param id: The ID of the Pasty.
        :type id: str
        :return: The Pasty with the specified ID, or None if not found.
        :rtype: Optional[Pasty]
        """
        for pasty in self.pasties:
            if pasty.id == id:
                return pasty

        return None

    def get_pasty_by_name(self, name: str) -> Optional[Pasty]:
        """
        Get a Pasty object by its name / title.

        :param name: The name of the Pasty object to retrieve.
        :type name: str
        :return: The Pasty object with the matching name, or None if not found.
        :rtype: Optional[Pasty]
        """
        for pasty in self.pasties:
            if pasty.title == name:
                return pasty

        return None

    @property
    def expires_in(self) -> ExpiresIn:
        """
        Get the value for when the paste is set to expire.

        :return: the `ExpiresIn` value of the paste
        :rtype: ExpiresIn
        """
        return self.__expires_in

    @property
    def is_private(self) -> bool:
        """
        Is the paste private.

        :return: True if the paste is private, False otherwise.
        :rtype: bool
        """
        return self.__is_private

    @property
    def is_public(self) -> bool:
        """
        Is the paste public.

        :return: True if the paste is public, False otherwise.
        :rtype: bool
        """
        return self.__is_public

    @property
    def tags(self) -> List[str]:
        """
        The tags of the paste

        :return: The list of tags associated with the object.
        :rtype: List[str]
        """
        return self.__tags

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the object to a dictionary representation.

        :return: A dictionary representing the object.
        :rtype: Dict[str, Any]
        """
        data: Dict[str, Any] = {
            "title": self.title,
            "expiresIn": self.expires_in.value,
            "isPrivate": self.is_private,
            "isPublic": self.is_public,
            "tags": ','.join(self.tags),
            "pasties": [pasty.to_dict() for pasty in self.pasties]
        }

        if hasattr(self, "id"):
            data["_id"] = self.id

        return data


class PasteResult(Paste):
    """
    A class representing the full object of a Paste
    """

    __slots__ = ("__id", "__owner_id", "__title", "__created_at", "__expires_in", "__deletes_at", "__stars", "__is_private", "__is_public", "__tags", "__pasties", "__edits", "__encrypted")

    @property
    def id(self) -> str:
        """
        Get the ID of the paste.

        :return: The ID of the paste.
        :rtype: str
        """
        return self.__id

    @property
    def owner_id(self) -> str:
        """
        Get the ID of the owner of the paste.

        :return: The owner ID as a string. If there's no owner, the ID is empty
        :rtype: str
        """
        return self.__owner_id

    @property
    def title(self) -> str:
        """
        Returns the title of the paste.

        :return: The title of the paste.
        :rtype: str
        """
        return self.__title

    @property
    def created_at(self) -> datetime:
        """
        Gets the date and time when the paste was created.

        :return: A datetime object representing the paste's creation time.
        :rtype: datetime.datetime
        """
        return self.__created_at

    @property
    def expires_in(self) -> ExpiresIn:
        """
        Get the value for when the paste is set to expire.

        :return: The expiration time of the object in the format of ExpiresIn.
        :rtype: ExpiresIn
        """
        return self.__expires_in

    @property
    def deletes_at(self) -> datetime:
        """
        Get the datetime of when the paste will be deleted.

        :return: The datetime the paste will be deleted from pastemyst.
        :rtype: datetime.datetime
        """
        return self.__deletes_at

    @property
    def stars(self) -> int:
        """
        Get the amount of people that has starred this paste.

        :return: The number of stars for the given object.
        :rtype: int
        """
        return self.__stars

    @property
    def is_private(self) -> bool:
        """
        Is the paste private.

        :return: True if the paste is private, False otherwise.
        :rtype: bool
        """
        return self.__is_private

    @property
    def is_public(self) -> bool:
        """
        Is the paste public.

        :return: True if the paste is public, False otherwise.
        :rtype: bool
        """
        return self.__is_public

    @property
    def tags(self) -> List[str]:
        """
        The tags of the paste

        :return: The list of tags associated with the object.
        :rtype: List[str]
        """
        return self.__tags

    @property
    def pasties(self) -> List[Pasty]:
        """
        Get the pasties of the paste.

        :return: A list of Pasty objects.
        :rtype: List[Pasty]
        """
        return self.__pasties

    @property
    def edits(self) -> List[PasteEdit]:
        """
        Returns the list of PasteEdits associated with this method.

        :return: A list of PasteEdit objects representing the edits made.
        :rtype: List[PasteEdit]
        """
        return self.__edits

    @property
    def is_encrypted(self) -> bool:
        """
        Is the paste is encrypted.

        :return: True if the paste is encrypted, False otherwise.
        :rtype: bool
        """
        return self.__encrypted

    @property
    def url(self) -> str:
        """
        Get the URL of the paste.

        :return: The URL of the paste.
        :rtype: str
        """
        return f"https://paste.myst.rs/{self.id}"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "PasteResult":
        """
        This static method creates a PasteResult object from the provided dictionary data. It iterates over the key-value pairs in the dictionary and performs certain transformations or mappings
        * based on the keys. The resulting PasteResult object is returned.

        The parameter `data` is expected to be a dictionary with string keys and values of any type.

        The return type is a PasteResult object.

        Example usage:
            data = {
                "created_at": 1609459200,
                "deletes_at": 1612051200,
                "_id": "12345",
                "expires_in": 3600,
                "pasties": [],
                "edits": []
            }
            paste = PasteResult.from_dict(data)

            print(paste.id)  # Output: "12345"
            print(paste.expires_in)  # Output: <expiry time>
            # ... Other attributes of the PasteResult object

        Note: Refer to the source code for exact details of transformations performed on keys and values.

        :param data: A dictionary containing the data for creating a PasteResult object.
        :type data: Dict[str, Any]
        :return: A PasteResult object created from the given dictionary.
        :rtype: PasteResult
        """
        paste: PasteResult = PasteResult()
        for key, value in data.items():
            key = camel_to_snake(key)

            if key in ("created_at", "deletes_at"):
                value = datetime.fromtimestamp(int(value), timezone.utc)
            elif key == "_id":
                key = "id"
            elif key == "expires_in":
                value = ExpiresIn(value)
            elif key in ("pasties", "edits"):
                if key == "pasties":
                    value = [raw if isinstance(raw, Pasty) else Pasty.from_dict(raw) for raw in value]
                    pass
                elif key == "edits":
                    value = [raw if isinstance(raw, PasteEdit) else PasteEdit.from_dict(raw) for raw in
                             value]

            paste.__setattr__(mangle_attr(paste, f"__{key}"), value)

        return paste
