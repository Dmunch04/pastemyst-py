import trio
import multio
from datetime import datetime

from pastemyst.api import HttpClient
from pastemyst.models import LanguageInfo, raw_paste_to_paste, ExpiresIn, User, RequestError


class Client:
    def __init__(self, key=None, is_dev=False):
        self.init_async()

        self.key = key
        self.is_dev = is_dev

        self.api = HttpClient(self)

    def init_async(self):
        multio.init('trio')

    def get_language_info(self, name=None, ext=None):
        raw = trio.run(self.api.get_language, name, ext)
        lang = LanguageInfo()
        lang.from_dict(raw)
        return lang

    def get_paste(self, paste_id):
        raw = trio.run(self.api.get_paste, paste_id)
        paste = raw_paste_to_paste(raw)

        return paste

    def create_paste(self, paste):
        if not paste.pasties:
            raise RequestError('there must be at least 1 pasty in a paste')

        raw = trio.run(self.api.create_paste, paste)
        paste = raw_paste_to_paste(raw)

        return paste

    def edit_paste(self, paste):
        raw = trio.run(self.api.edit_paste, paste)
        paste = raw_paste_to_paste(raw)

        return paste

    def delete_paste(self, paste_id):
        code = trio.run(self.api.delete_paste, paste_id)
        if code == 200:
            return True
        else:
            return False

    def get_expire_stamp(self, paste):
        if not paste.expires_in:
            raise RequestError('paste must have expires_in field')

        if not paste.created_at:
            raise RequestError('paste must have created_at field')

        if paste.expires_in == ExpiresIn.NEVER:
            raise RequestError('cant find expiration stamp of paste that never expires')

        unix_stamp = (datetime.fromtimestamp(paste.created_at.timestamp()) - datetime(1970, 1, 1)).total_seconds()
        raw = trio.run(self.api.get_expire_unix, int(unix_stamp), paste.expires_in)
        return datetime.utcfromtimestamp(int(raw['result']))

    def user_exists(self, username):
        code = trio.run(self.api.get_user_exists, username)
        if code == 200:
            return True
        else:
            return False

    def get_user(self, username):
        raw = trio.run(self.api.get_user, username)

        user = User()
        user.from_dict(raw)

        return user
