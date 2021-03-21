from pastemyst.utils import spacify_string


class User:
    __slots__ = (
        '_id', 'id', 'username', 'avatar_url',
        'default_lang', 'public_profile',
        'supporter_length', 'contributor'
    )

    def from_dict(self, data):
        for attr in data:
            if attr == '_id':
                setattr(self, 'id', data[attr])

            setattr(self, spacify_string(attr), data[attr])
