from pastemyst import Client, User


def test_user_exists():
    client: Client = Client()
    user_exists: bool = client.user_exists("munchii")
    assert user_exists is True


def test_get_user():
    client: Client = Client()
    user: User = client.get_user("munchii")
    assert user.username == "munchii"
    assert user.is_contributor is True
    assert user.is_public_profile is True
