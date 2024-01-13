from pastemyst import *
from json import loads, dumps


class DataStorage:
    def __init__(self, key: str, paste_id: str):
        self.client = Client(key)
        self.paste_id = paste_id
        self.data = {}

        if self.paste_id is None or not self.client.paste_exists(self.paste_id):
            self.paste_id = self.init_paste().id
            print(self.paste_id)

        self.paste = self.client.get_paste(self.paste_id)

        self.init_data()

    def init_paste(self) -> Paste:
        return self.client.create_paste(
            Paste(
                title="DataStorage",
                pasties=[Pasty(title="storage.data", language=Language.JSON, code="{}")],
                expires_in=ExpiresIn.ONE_HOUR  # probably wanna change this
            )
        )

    def init_data(self) -> None:
        self.data = loads(self.client.get_paste(self.paste_id).pasties[0].code)

    def save(self) -> None:
        self.paste.pasties[0].code = dumps(self.data)
        self.paste = self.client.edit_paste(self.paste)


if __name__ == "__main__":
    # you must set the key
    store: DataStorage = DataStorage(key=None, paste_id="")
    store.data["scoreboard"] = {
        "Daniel": 100,
        "Bob": 69
    }
    store.save()

    print(store.paste_id)
