from comms import CommsListener

# example game user
creds = {
    "exchange": "battleship",
    "port": "5672",
    "host": "battleshipgame.fun",
    "user": "poseidon",
    "password": "kQKrBuvvUqiQ",
    "hash": "53097245371629879277695268655844287964"
  }

print("Comms Listener starting. To exit press CTRL+C ...")
# create instance of the listener class and sending in the creds
# object as kwargs
commsListener = CommsListener(**creds)

# tell rabbitMQ which 'topics' you want to listen to. In this case anything
# with the team name in it (user) and the broadcast keyword.
commsListener.bindKeysToQueue([f"#.{creds['user']}.#", "#.broadcast.#"])

# now really start listening
commsListener.startConsuming()