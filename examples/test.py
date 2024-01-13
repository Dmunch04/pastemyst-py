import time

from pastemyst import Client, Paste, PasteResult, Pasty, ExpiresIn


client = Client("your_token")
pastes = client.get_self_user_pastes()
for paste in pastes:
    #print(paste.title)
    pass
user = client.get_self_user()
print(user.username)
print(user.is_public_profile)

new_client = Client()
paste = Paste(title="yeeeeeet", pasties=[Pasty(title="hello", code="world")], expires_in=ExpiresIn.ONE_HOUR)
paste = client.create_paste(paste)
print(paste.id)
print(paste.title)
print(paste.url)
paste.pasties[0].code = "hello, world"
time.sleep(5)
client.edit_paste(paste)
print("edited")
