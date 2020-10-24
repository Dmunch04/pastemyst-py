class HttpError(Exception):
    def __init__(self, res, data):
        self.res = res
        self.status = res.status_code
        self.reason = res.reason_phrase
        self.method = res.method
        self.code = data.get('code', 0)
        self.message = data.get('message', '')

        error = '{0.reason} ({0.status}): {0.message}'

        super().__init__(error.format(self))


class RequestError(Exception):
    pass