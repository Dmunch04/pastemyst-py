from pastemyst import Client, LanguageInfo, Language


def test_get_by_name():
    client: Client = Client()
    language: LanguageInfo = client.get_language_info(name="Python")
    assert language.name == "Python" == Language.PYTHON
    assert "py" in language.extensions


def test_get_by_extension():
    client: Client = Client()
    language: LanguageInfo = client.get_language_info(extension="py")
    assert language.name == "Python" == Language.PYTHON
    assert "py" in language.extensions
