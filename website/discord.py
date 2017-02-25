from flask import session, abort
from flask import current_app as app
from requests_oauthlib import OAuth2Session
import requests

DISCORD_API_URL 		= 'https://discordapp.com/api'
DISCORD_AUTH_BASE_URL   = DISCORD_API_URL + '/oauth2/authorize'
DISCORD_TOKEN_URL       = DISCORD_API_URL + '/oauth2/token'

def token_updater(token):
	session['auth_token'] = token

def make_session(token=None, state=None):
	client_id = app.config['DISCORD_CLIENT_ID']
	secret = app.config['DISCORD_SECRET_KEY']
	return OAuth2Session(
		client_id=client_id,
		token=token,
		state=state,
		scope=['identify', 'connections'],
		token_updater=token_updater,
		auto_refresh_url=DISCORD_TOKEN_URL,
		auto_refresh_kwargs={
			'client_id': client_id,
			'client_secret': secret
		},
		redirect_uri=app.config['REDIRECT_URI'])

def get_twitch_name():
	token = session.get('auth_token')
	if token is None:
		return None
	
	with make_session(token=token) as discord:
		endpoint = DISCORD_API_URL + '/users/@me/connections'
		#headers = {'Authorization': 'Bearer %s' % token }
		resp = discord.get(endpoint)
		if resp.status_code != 200:
			session.pop('auth_token')
			return None

		data = resp.json()
		for entry in data:
			if entry['type'] == 'twitch':
				return entry['name']
		return '__not_linked!'

def get_user():
	token = session.get('auth_token')
	if token is None:
		abort(401, 'null token in get_user')

	with make_session(token=token) as discord:
		endpoint = DISCORD_API_URL + '/users/@me'
		user = discord.get(endpoint)
		if user.status_code == 401:
			session.pop('auth_token')
			abort(401, 'discord rejected bearer token')

		data = user.json()
		return data['id']

def add_role():
	user_id = get_user()
	if user_id is None:
		abort(400, 'unable to get a user id')

	endpoint = DISCORD_API_URL + '/guilds/{guild}/members/{user}/roles/{role}'.format(
		guild = app.config['GUILD'],
		user = user_id,
		role = app.config['ROLE'])

	token = app.config['DISCORD_BOT_TOKEN']
	headers = {'Authorization': 'Bot %s' % token}

	resp = requests.put(endpoint, headers=headers)
	if resp.status_code != 204:
		abort(400, 'got a {code} adding role'.format(code=resp.status_code))
	else:
		return True