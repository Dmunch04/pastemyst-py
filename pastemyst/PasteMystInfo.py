import datetime
import urllib.parse

from PasteMyst import BaseURL

class PasteMystInfo (object):
    def __init__ (self, ID: str, CreatedAt: float, Code: str, ExpiresIn: str, Language: str):
        self.ID = ID
        self.CreatedAt = datetime.datetime.fromtimestamp (CreatedAt)
        self.Code = urllib.parse.unquote (Code)
        self.ExpiresIn = ExpiresIn
        self.Language = Language

        self.id = ID
        self.created_at = CreatedAt
        self.code = Code
        self.expires_in = ExpiresIn
        self.language = Language

        self.URL = BaseURL + ID
        self.url = BaseURL + ID