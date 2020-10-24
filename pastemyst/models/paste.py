from datetime import datetime

from pastemyst.models.language import Language
from pastemyst.utils import spacify_string


class ExpiresIn:
    ONE_HOUR = '1h'
    TWO_HOURS = '2h'
    TEN_HOURS = '10h'
    ONE_DAY = '1d'
    TWO_DAYS = '2d'
    ONE_WEEK = '1w'
    ONE_MONTH = '1m'
    ONE_YEAR = '1y'
    NEVER = 'never'


class EditType:
    TITLE = 0
    PASTY_TITLE = 1
    PASTY_LANGUAGE = 2
    PASTY_CONTENT = 3
    PASTY_ADDED = 4
    PASTY_REMOVED = 5


class Sendable(object):
    @classmethod
    def to_dict(cls):
        raise NotImplementedError()

    def from_dict(self, data):
        for attr in data:
            setattr(self, spacify_string(attr), data[attr])


class Paste(Sendable):
    __slots__ = (
        '_id', 'owner_id', 'title',
        'created_at', 'expires_in', 'deletes_at',
        'stars', 'is_private', 'is_public',
        'tags', 'pasties', 'edits'
    )

    def __init__(self, title='untitled', pasties=[], expires_in=ExpiresIn.NEVER, is_private=False, is_public=True, tags=[]):
        self.title = title
        self.pasties = pasties
        self.expires_in = expires_in
        self.is_private = is_private
        self.is_public = is_public
        self.tags = tags

    def __setattr__(self, key, value):
        if key in ('created_at', 'deletes_at'):
            value = datetime.utcfromtimestamp(int(value))

        super().__setattr__(key, value)

    def to_dict(self):
        data = {
            'title': self.title,
            'expiresIn': self.expires_in,
            'isPrivate': self.is_private,
            'isPublic': self.is_public,
            'tags': ','.join(self.tags),
            'pasties': [pasty.to_dict() for pasty in self.pasties]
        }

        if hasattr(self, '_id'):
            data['_id'] = self._id

        return data


class Pasty(Sendable):
    __slots__ = (
        '_id', 'language', 'title', 'code'
    )

    def __init__(self, title='untitled', code='', language=Language.AUTODETECT):
        self.title = title
        self.code = code
        self.language = language

    def to_dict(self):
        data = {
            'language': self.language,
            'title': self.title,
            'code': self.code
        }

        if hasattr(self, '_id'):
            data['_id'] = self._id

        return data


class PasteEdit(Sendable):
    __slots__ = (
        '_id', 'edit_id', 'edit_type',
        'metadata', 'edit', 'editedAt'
    )

    def __setattr__(self, key, value):
        if key == 'edited_at':
            value = datetime.utcfromtimestamp(int(value))

        super().__setattr__(key, value)


def raw_paste_to_paste(raw):
    pasties_raw = raw.get('pasties', [])
    edits_raw = raw.get('edits', [])
    del raw['pasties']
    del raw['edits']

    paste = Paste()
    paste.from_dict(raw)
    paste.pasties = []
    paste.edits = []

    for raw_pasty in pasties_raw:
        pasty = Pasty()
        pasty.from_dict(raw_pasty)
        paste.pasties.append(pasty)

    for raw_edit in edits_raw:
        edit = PasteEdit()
        edit.from_dict(raw_edit)
        paste.edits.append(edit)

    return paste
