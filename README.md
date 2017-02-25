# followerbridge

A small tool to offer perks for your [twitch.tv](https://twitch.tv) followers on [Discord](https://discordapp.com)

### Example

A sample is running on [followerbridge.foxbot.me](https://followerbridge.foxbot.me)

### Requirements
- Python 3
- Flask

`pip install -r requirements.txt`

### Running

Make a `config.py` file in the root directory with the following variables:
```py
SERVER_NAME = 'localhost:80' # set a port

DISCORD_CLIENT_ID = 'client ID of oauth application'
DISCORD_SECRET_KEY = 'client secret of oauth application'
DISCORD_BOT_TOKEN = 'token of bot account for application'
REDIRECT_URI = 'redirect uri of application - https://my.website/discord' # domain/discord
TWITCH_NAME = 'the name of your twitch account'
TWITCH_API_KEY = 'a twitch oauth app api key'

GUILD = 'the id of your discord guild'
ROLE = 'the id of the follower role in your discord guild'
INVITE = 'a link to an invite to your discord guild'

SECRET_KEY = DISCORD_SECRET_KEY # leave this field as is
```

Next, run `$ python3 run.py`

