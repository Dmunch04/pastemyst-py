from multio import asynclib


class API:
    HOST = 'https://paste.myst.rs'
    BETA_HOST = 'https://pmb.myst.rs'
    API_VERSION = '2'
    HTTP_ENDPOINT = f'{HOST}/api/v{API_VERSION}'
    BETA_HTTP_ENDPOINT = f'{BETA_HOST}/api/v{API_VERSION}'


async def run_later(time, task):
    await asynclib.sleep(time)
    return await task


def spacify_string(s):
    w = []
    cur = ''
    for c in s:
        if c.isupper():
            w.append(cur)
            cur = ''
            cur += c.lower()
        else:
            cur += c
    w.append(cur)
    return '_'.join(w)
