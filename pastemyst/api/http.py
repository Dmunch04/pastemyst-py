import json
import time

import httpx
from httpx import Response
import trio
from collections import defaultdict
from enum import Enum
from typing import Dict, Any, Coroutine, List

from .locks import HoldableLock, GlobalLock
from pastemyst.constants import API
from pastemyst.__version__ import __version__
from pastemyst.utils import run_later
from pastemyst.models import HttpError, PastemystError, RequestError, Paste


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class HttpClient:
    __slots__ = ("key", "is_dev", "retries", "buckets", "global_event", "http_endpoint", "headers", "session")

    def __init__(self, key: str = "", is_dev: bool = False):
        self.key = key
        self.is_dev = is_dev
        self.retries = 5
        self.buckets = defaultdict(trio.Lock)
        self.global_event = trio.Event()

        self.http_endpoint = API.BETA_HTTP_ENDPOINT if self.is_dev else API.HTTP_ENDPOINT

        self.headers = {
            "User-Agent": "PastemystPy ({})".format(__version__),
            "content-type": "application/json"
        }

        if self.key:
            self.headers["Authorization"] = self.key

        self.session = httpx.AsyncClient(headers=self.headers)

    def auth(self, key: str) -> None:
        self.key = key
        self.headers["Authorization"] = self.key
        self.session.headers = self.headers

    @property
    def is_authenticated(self) -> bool:
        return self.key is not None and self.key != ""

    async def request(self, method: HttpMethod, endpoint: str, **kwargs) -> Dict[str, Any] | int:
        bucket: str = f"{method.value}.{endpoint}"
        endpoint = self.http_endpoint + (endpoint if endpoint.startswith("/") else f"/{endpoint}")

        lock: trio.Lock = self.buckets[bucket]

        data: Dict[str, Any] | str | bytes = kwargs.get("data")
        if data is not None:
            if isinstance(data, dict):
                data = json.dumps(data)
            if isinstance(data, str):
                data = data.encode("utf-8")

        json_data: Dict[str, Any] | str = kwargs.get("json", {})

        if self.global_event.is_set():
            await self.global_event.wait()

        async with HoldableLock(lock) as hold_lock:
            async with trio.open_nursery() as nursery:
                for tries in range(self.retries):
                    response: Response = await self.session.request(method.value, endpoint, headers=self.headers, data=data, json=json_data)

                    res_data: str | Dict[str, Any] = response.text
                    if "application/json" in response.headers["content-type"]:
                        res_data = json.loads(res_data)

                    remaining: int = int(response.headers.get("X-Ratelimit-Remaining", 0))

                    if remaining == 0 and response.status_code != 429:
                        #hold_lock.hold()
                        #delay: float = int(response.headers.get("X-Ratelimit-Reset")) - time.time()
                        #nursery.start_soon(run_later, delay, lock.release())
                        pass
                    elif response.status_code == 429:
                        if data is not None:
                            with GlobalLock(self.global_event, data.get("global", False)):
                                retry_after: int = int(res_data.get("retry-after", 0))

                    if bool(kwargs.get("return_code", False)):
                        return response.status_code
                    elif 300 > response.status_code >= 200:
                        return res_data or None
                    elif response.status_code in (403, 404):
                        raise HttpError(response, res_data)
                    elif response.status_code in (500, 502):
                        await trio.sleep(1 + tries * 2)
                        continue
                    else:
                        raise HttpError(response, res_data)

        raise PastemystError(f"failed https request: {response.status_code} {method.value} {endpoint} : {response.text}")

    async def get(self, endpoint: str, **kwargs) -> Dict[str, Any] | int:
        return await self.request(HttpMethod.GET, endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs) -> Dict[str, Any] | int:
        return await self.request(HttpMethod.POST, endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs) -> Dict[str, Any] | int:
        return await self.request(HttpMethod.PUT, endpoint, **kwargs)

    async def patch(self, endpoint: str, **kwargs) -> Dict[str, Any] | int:
        return await self.request(HttpMethod.PATCH, endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs) -> Dict[str, Any] | int:
        return await self.request(HttpMethod.DELETE, endpoint, **kwargs)

    def get_language(self, name: str = None, extension: str = None) -> Coroutine[Any, Any, Dict[str, Any] | int | None]:
        if name is not None:
            route: str = f"/data/language?name={name}"
        elif name is None and extension is not None:
            route: str = f"/data/languageExt?extension={extension}"
        else:
            raise RequestError("invalid arguments. must provide language name or extension")

        return self.get(route)

    def get_paste(self, paste_id: str) -> Coroutine[Any, Any, Dict[str, Any] | int | None]:
        if paste_id is None or paste_id == "":
            raise RequestError("invalid arguments. must provide a paste id to look up")

        route: str = f"/paste/{paste_id}"
        return self.get(route)

    def create_paste(self, paste: Paste) -> Coroutine[Any, Any, Dict[str, Any] | int | None]:
        route: str = f"/paste"
        payload: Dict[str, Any] = paste.to_dict()

        if not self.is_authenticated:
            del payload["isPrivate"]
            del payload["isPublic"]
            del payload["tags"]

        return self.post(route, json=payload)

    def edit_paste(self, paste: Paste, target_id: str = None) -> Coroutine[Any, Any, Dict[str, Any] | int | None]:
        payload: Dict[str, Any] = paste.to_dict()

        if "_id" not in payload:
            if not target_id:
                raise RequestError("invalid arguments. missing _id field or target_id")
            payload["_id"] = target_id

        if not ("_id" in pasty for pasty in payload["pasties"]):
            raise RequestError("invalid arguments. missing _id field in pasty")

        route: str = f"/paste/{payload["_id"]}"

        return self.patch(route, json=payload)

    def delete_paste(self, paste_id: str) -> Coroutine[Any, Any, Dict[str, Any] | int | None]:
        route: str = f"/paste/{paste_id}"
        return self.delete(route, return_code=True)

    # TODO: type-hint
    def get_expire_unix(self, created_at, expires_in) -> Coroutine[Any, Any, Dict[str, Any] | int | None]:
        route: str = f"/time/expiresInToUnixTime?createdAt={created_at}&expiresIn={expires_in}"
        return self.get(route)

    def get_user_exists(self, username: str) -> Coroutine[Any, Any, Dict[str, Any] | int | None]:
        route: str = f"/user/{username}/exists"
        return self.get(route, return_code=True)

    def get_user(self, username: str) -> Coroutine[Any, Any, Dict[str, Any] | int | None]:
        route: str = f"/user/{username}"
        return self.get(route)

    def get_self(self) -> Coroutine[Any, Any, Dict[str, Any] | int | None]:
        route: str = "/user/self"

        if not self.is_authenticated:
            raise RequestError("must be authenticated (provide api key), to access self user")

        return self.get(route)

    def get_self_pastes(self) -> Coroutine[Any, Any, Dict[str, Any] | List[str] | int | None]:
        route: str = "/user/self/pastes"

        if not self.is_authenticated:
            raise RequestError("must be authenticated (provide api key), to access self user")

        return self.get(route)
