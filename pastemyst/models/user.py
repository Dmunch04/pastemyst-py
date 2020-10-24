from pastemyst.utils import spacify_string


class User:
    __slots__ = (
        '_id', 'username', 'avatar_url',
        'default_lang', 'public_profile',
        'supporter_length'
    )

    def from_dict(self, data):
        for attr in data:
            setattr(self, spacify_string(attr), data[attr])