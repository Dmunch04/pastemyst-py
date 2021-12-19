from json import loads, dumps
from pastemyst import *

# you would want to set your key here
# note: saving work if you dont set the key
client = Client(key=None)
paste = None

def store_data(name, data):
  return client.create_paste(
    Paste(
      title=name,
      pasties=[
        Pasty(
          title=name,
          code=dumps(data),
          language=Language.JSON
        )
      ],
      # you would probably wanna change this to never
      expires_in=ExpiresIn.ONE_HOUR
    )
  )

def get_data(id):
  return loads(
    client.get_paste(id).pasties[0].code
  )

def save_data(data):
  paste.pasties[0].code = dumps(data)
  return client.edit_paste(paste)

if __name__ == '__main__':
  xp_data = {
    'leaderboard': {
      'John': 10,
      'Joe': 20,
      'Daniel': 69
    }
  }
  paste = store_data("xp.json", xp_data)
  id = paste._id

  # ...

  data = get_data(id)
  leaderboard = data['leaderboard']
  print(leaderboard)

  # this only works if you have set the api key
  leaderboard['Joe'] += 1
  data['leaderboard'] = leaderboard
  save_data(leaderboard)
