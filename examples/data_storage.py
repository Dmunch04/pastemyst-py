import json
import time
from typing import Callable, Any, Dict

from pastemyst import *


class DataStorage:
    def __init__(
            self,
            key: str,
            paste_id: str,
            decode_fn: Callable[[str, ...], Any] = json.loads,
            encode_fn: Callable[[Dict[str, Any], ...], str] = json.dumps
    ):
        self.client = Client(key)
        self.paste_id = paste_id
        self.decode_fn = decode_fn
        self.encode_fn = encode_fn

        self.data: Dict[str, Any] = {}

        if self.paste_id is None or not self.client.paste_exists(self.paste_id):
            self.paste_id = self.init_paste().id

        self.paste: PasteResult = self.client.get_paste(self.paste_id)

        self.init_data()

    def init_paste(self) -> PasteResult:
        return self.client.create_paste(
            Paste(
                title="DataStorage",
                pasties=[Pasty(title="storage.data", language=Language.JSON, code="{}")],
                expires_in=ExpiresIn.ONE_HOUR  # probably wanna change this
            )
        )

    def init_data(self) -> None:
        self.data = self.decode_fn(self.client.get_paste(self.paste_id).pasties[0].code)

    def save(self) -> None:
        self.paste.pasties[0].code = self.encode_fn(self.data)
        self.paste = self.client.edit_paste(self.paste)

    def get(self, key: str) -> Any:
        return self.data[key]

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.save()


if __name__ == "__main__":
    # you must set the key
    store: DataStorage = DataStorage(key="", paste_id="")
    store.data["counter"] = 0
    with store:
        for i in range(100):
            store.data["counter"] += 1

    print("done")
    time.sleep(10)

    with store:
        for i in range(100):
            store.data["counter"] += 1

    print("done")
