from flask import current_app as app
import requests

TWITCH_ENDPOINT_FORMAT='https://api.twitch.tv/kraken/users/{channel}/follows/channels/{target}'

def is_following(user):
	target = app.config['TWITCH_NAME']
	endpoint = TWITCH_ENDPOINT_FORMAT.format(channel=user, target=target)
	headers = {'Client-ID': app.config['TWITCH_API_KEY']}
	
	r = requests.get(endpoint, headers=headers)
	if r.status_code == 404:
		return False
	elif r.status_code == 200:
		return True
	else:
		return None