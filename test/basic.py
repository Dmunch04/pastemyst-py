from pastemyst import init, Client, Language, Paste, Pasty, ExpiresIn, EditType

if __name__ == '__main__':
    init('trio')
    client = Client(key='', is_dev=True)

    res1 = client.get_paste('50ry40it')
    assert len(res1.pasties) == 1
    assert res1.pasties[0].title == 'basic.py'
    assert res1.pasties[0].language == Language.PYTHON

    res2 = client.get_paste('8czo099x')
    assert len(res2.pasties) == 2
    assert res2.pasties[0].title == 'file1.py'
    assert res2.pasties[1].title == 'file2.py'
    assert res2.pasties[0].language == Language.PYTHON
    assert res2.pasties[1].language == Language.PYTHON

    res3 = client.get_language_info('d')
    assert res3.name == 'D'
    assert res3.color == '#ba595e'

    res4 = client.create_paste(Paste(pasties=[Pasty('titly', 'print("a")')], expires_in=ExpiresIn.ONE_HOUR))
    assert res4.title == 'untitled'
    assert len(res4.pasties) == 1
    assert res4.expires_in == ExpiresIn.ONE_HOUR

    res4.title = 'yeet'
    res5 = client.edit_paste(res4)
    assert len(res5.edits) == 1
    assert res5.edits[0].edit_type == EditType.TITLE

    res6 = client.delete_paste(res4._id)
    assert res6

    res7 = client.get_expire_stamp(res4)
    assert res7
    assert res7 == res4.deletes_at

    res8 = client.user_exists('munchii')
    assert res8

    res9 = client.get_user('munchii')
    assert res9.public_profile
    assert res9.default_lang == 'Autodetect'
