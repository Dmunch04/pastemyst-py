import random
import time
from typing import List

from pastemyst import *


BASE_36_CHARS: str = "0123456789abcdefghijklmnopqrstuvwxyz"

client: Client = Client()


def encode_base_36(number: int) -> str:
    result: str = ""
    temp: int = number
    while temp != 0:
        result += BASE_36_CHARS[temp % 36]
        temp //= 36

    return result


def random_base36_id() -> str:
    return encode_base_36(int(random.uniform(78_364_164_096, 2_821_109_907_455)))


def generate_id() -> str:
    new_id: str = ""
    for i in range(8):
        new_id += random.choice(BASE_36_CHARS)
    return new_id


def paste_exists(paste_id: str) -> bool:
    return client.paste_exists(paste_id)


def run():
    pastes: List[PasteResult] = []
    i: int = 0
    while i < 1_000_000:
        #pid = generate_id()
        pid = random_base36_id()
        print(f"looking for {pid}")
        if paste_exists(pid):
            paste: PasteResult = client.get_paste(pid)
            pastes.append(paste)
            print(f"--- -- found paste: {pid}")
        i += 1
        time.sleep(0.25)

    print(pastes)


if __name__ == "__main__":
    run()
