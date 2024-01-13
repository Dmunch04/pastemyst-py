from pastemyst import Client, Paste, Pasty, Language, ExpiresIn


def test_get_paste():
    client: Client = Client()
    paste: Paste = client.get_paste("21y82rbw")
    assert len(paste.pasties) == 1
    assert paste.pasties[0].title == "shellsort.adb"
    assert paste.pasties[0].language == Language.JAVASCRIPT


def test_create_paste():
    client: Client = Client()
    paste: Paste = Paste(
        title="example paste",
        pasties=[
            Pasty(title="example.py", code="print('hello')", language=Language.PYTHON)
        ],
        expires_in=ExpiresIn.ONE_HOUR
    )

    # remember to reassign or assign the result to another variable, to access fields such as the paste's id
    paste = client.create_paste(paste)
    assert paste.title == "example paste"
    assert len(paste.pasties) == 1
    assert paste.pasties[0].title == "example.py"
    assert paste.pasties[0].language == Language.PYTHON
