class HttpError(Exception):
    def __init__(self, res, data):
        self.res = res
        self.status = res.status_code
        self.reason = res.reason_phrase
        self.method = res.method
        if isinstance(data, dict):
            self.message = data.get('statusMessage', '')
        else:
            self.message = str(data)

        error = '{0.reason} ({0.status}): {0.message}'

        super().__init__(error.format(self))


class RequestError(Exception):
    pass
