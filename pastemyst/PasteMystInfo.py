import datetime
import json
import urllib.parse

class PasteMystInfo (object):
    def __init__ (self, ID: str, CreatedAt: float, Code: str, ExpiresIn: str, Language: str, BaseURL: str):
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

    def __str__ (self):
        return json.dumps ({
            'id': self.ID,
            'createdAt': self.CreatedAt.__str__ (),
            'code': self.Code,
            'expiresIn': self.ExpiresIn,
            'language': self.language,
            'url': self.URL
        })

    def __repr__ (self):
        return self.__str__ ()