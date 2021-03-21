from pastemyst import Client, Language, Paste, Pasty, ExpiresIn, EditType

if __name__ == '__main__':
    client = Client(key='')

    res1 = client.get_paste('21y82rbw')
    assert len(res1.pasties) == 1
    assert res1.pasties[0].title == 'shellsort.adb'
    assert res1.pasties[0].language == Language.JAVASCRIPT

    res2 = client.get_paste('flzf1gcd')
    assert len(res2.pasties) == 3
    assert res2.pasties[0].title == 'pmdeps'
    assert res2.pasties[1].title == 'app.d'
    assert res2.pasties[2].title == 'hello.d'
    assert res2.pasties[0].language == Language.CPP
    assert res2.pasties[1].language == Language.D
    assert res2.pasties[1].language == Language.D

    res3 = client.get_language_info('d')
    assert res3.name == 'D'
    assert res3.color == '#ba595e'

    res4 = client.create_paste(Paste(pasties=[Pasty('titly', 'print("a")')], expires_in=ExpiresIn.ONE_HOUR))
    assert res4.title == 'untitled'
    assert len(res4.pasties) == 1
    assert res4.expires_in == ExpiresIn.ONE_HOUR

    res5 = client.get_expire_stamp(res4)
    assert res5
    assert res5 == res4.deletes_at

    res6 = client.user_exists('munchii')
    assert res6

    res7 = client.get_user('munchii')
    assert res7.public_profile
    assert res7.default_lang == 'Autodetect'
    assert res7.contributor
