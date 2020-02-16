import json
import requests
import urllib.parse

from .PasteMystInfo import PasteMystInfo

BaseURL = 'https://paste.myst.rs/'
APIURL = BaseURL + 'api'

def CreatePasteMyst (Code: str, ExpiresIn: str = 'never', Language: str = None):
    Payload = {
        'code': urllib.parse.quote(Code),
        'expiresIn': ExpiresIn,
    }

    if Language:
        Payload['language'] = Language

    Headers = {
        'content-type': 'application/json'
    }

    Response = requests.post (APIURL + '/paste', data = json.dumps (Payload), headers = Headers, verify = False).json ()

    return MakeObject (Response)

def create_paste_myst (code: str, expires_in: str = 'never', language: str = None):
    return CreatePasteMyst (code, expires_in, language)

def GetPasteMyst (ID: str):
    Response = requests.get (APIURL + '/paste?id=' + ID, data = {}, headers = {}, verify = False).json ()

    return MakeObject (Response)

def get_paste_myst (id: str):
    return GetPasteMyst (id)

def MakeObject (Response: dict):
    return PasteMystInfo (
        Response['id'],
        Response['createdAt'],
        Response['code'],
        Response['expiresIn'],
        Response['language'],
        BaseURL
    )