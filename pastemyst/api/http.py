import time
import json
import asks
import trio
from collections import defaultdict

from pastemyst.utils import API, run_later
from pastemyst.models import HttpError, RequestError


class RequestMethod:
    POST = 'POST'
    GET = 'GET'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'


class HoldableLock:
    __slots__ = ('lock', 'unlock')

    def __init__(self, lock):
        self.unlock = True
        self.lock = lock

    def hold(self):
        self.unlock = False

    async def __aenter__(self):
        await self.lock.acquire()
        return self

    async def __aexit__(self, *args):
        if self.unlock:
            self.lock.release()


class GlobalLock:
    __slots__ = ('global_event', 'is_global')

    def __init__(self, global_event, is_global):
        self.is_global = is_global
        self.global_event = global_event

    def __enter__(self):
        if self.is_global:
            self.global_event.clear()

    def __exit__(self, *args):
        if self.is_global:
            self.global_event.set()


class HttpClient:
    def __init__(self, client=None):
        self.client = client
        self.key = client.key
        self.is_dev = client.is_dev or False
        self.retries = 5
        self.buckets = defaultdict(trio.Lock)
        self.global_event = trio.Event()

        self.http_endpoint = API.BETA_HTTP_ENDPOINT if self.is_dev else API.HTTP_ENDPOINT

        self.headers = {
            'User-Agent': 'PasteMystBot (v1.0)',
            'content-type': 'application/json'
        }

        if self.key:
            self.headers['Authorization'] = self.key

        self.session = asks.Session(headers=self.headers)

    async def request(self, method, endpoint, **kwargs):
        bucket = f'{method}.{endpoint}'
        endpoint = self.http_endpoint + endpoint

        lock = self.buckets[bucket]

        data = kwargs.get('data')
        if data is not None:
            if isinstance(data, dict):
                data = json.dumps(data)
            if isinstance(data, str):
                data = data.encode('utf-8')

        json_data = kwargs.get('json')

        if self.global_event.is_set():
            await self.global_event.wait()

        async with HoldableLock(lock) as hold_lock:
            async with trio.open_nursery() as nursery:
                for tries in range(self.retries):
                    res = await self.session.request(method, endpoint, headers=self.headers, data=data, json=json_data)

                    data = res.text
                    if 'application/json' in res.headers['content-type']:
                        data = json.loads(data)
                    remaining = res.headers.get('X-Ratelimit-Remaining', 0)

                    if remaining == '0' and res.status_code != 429:
                        hold_lock.hold()
                        delay = int(res.headers.get('X-Ratelimit-Reset')) - time.time()
                        nursery.start_soon(run_later, delay, lock.release())
                    elif res.status_code == 429:
                        with GlobalLock(self.global_event, data.get('global', False)):
                            retry_after = data.get('retry-after', 0)
                            await trio.sleep(retry_after / 1000.0)
                        continue

                    if bool(kwargs.get('return_code', False)):
                        return res.status_code
                    elif 300 > res.status_code >= 200:
                        return data or None
                    elif res.status_code in (403, 404):
                        raise HttpError(res, data)
                    elif res.status_code in (500, 502):
                        await trio.sleep(1 + tries * 2)
                        continue
                    else:
                        raise HttpError(res, data)

        raise Exception(f'Failed HTTP Request: {res.status_code} {method} {endpoint}')

    async def post(self, endpoint, **kwargs):
        return await self.request(RequestMethod.POST, endpoint, **kwargs)

    async def get(self, endpoint, **kwargs):
        return await self.request(RequestMethod.GET, endpoint, **kwargs)

    async def put(self, endpoint, **kwargs):
        return await self.request(RequestMethod.PUT, endpoint, **kwargs)

    async def patch(self, endpoint, **kwargs):
        return await self.request(RequestMethod.PATCH, endpoint, **kwargs)

    async def delete(self, endpoint, **kwargs):
        return await self.request(RequestMethod.DELETE, endpoint, **kwargs)

    def get_language(self, name=None, ext=None):
        if name is not None:
            route = f'/data/language?name={name}'
        elif name is None and ext is not None:
            route = f'/data/languageExt?extension={ext}'
        else:
            raise RequestError('no name or extension given')

        return self.get(route)

    def get_paste(self, paste_id):
        route = f'/paste/{paste_id}'
        return self.get(route)

    def create_paste(self, paste):
        route = f'/paste'
        payload = paste.to_dict()

        if not self.key:
            del payload['isPrivate']
            del payload['isPublic']
            del payload['tags']

        return self.post(route, json=payload)

    def edit_paste(self, paste):
        route = f'/paste/{paste._id}'
        payload = paste.to_dict()

        if not '_id' in payload:
            raise RequestError('no _id field in paste')

        if not ('_id' in pasty for pasty in payload['pasties']):
            raise RequestError('no _id field in pasty')

        return self.patch(route, json=payload)

    def delete_paste(self, paste_id):
        route = f'/paste/{paste_id}'
        return self.delete(route, return_code=True)

    def get_expire_unix(self, created_at, expires_in):
        route = f'/time/expiresInToUnixTime?createdAt={created_at}&expiresIn={expires_in}'
        return self.get(route)

    def get_user_exists(self, username):
        route = f'/user/{username}/exists'
        return self.get(route, return_code=True)

    def get_user(self, username):
        route = f'/user/{username}'
        return self.get(route)
