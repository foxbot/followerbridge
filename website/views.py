from flask import current_app as app
from flask import Blueprint, render_template
from flask import session, request
from flask import redirect, url_for, abort
from werkzeug.routing import RequestRedirect

from .discord import make_session, get_twitch_name, add_role, DISCORD_AUTH_BASE_URL, DISCORD_TOKEN_URL
from .twitch import is_following

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('index.html', title='home', streamer=app.config['TWITCH_NAME'], discord=app.config['INVITE'], linked=session.get('linked'))

@main.route('/error/twitch_unlinked')
def twitch_unlinked():
	return render_template('error.html', title='error', desc='your discord account must be linked to twitch to continue')

@main.route('/error/twitch')
def twitch_error():
	return render_template('error.html', title='error', desc='oops, we had some kind of error communicating with the Twitch API')

@main.route('/error/follow')
def follow():
	return render_template('follow.html', title='not following', streamer=app.config['TWITCH_NAME'])

@main.route('/error/discord')
def discord_error():
	return render_template('error.html', title='error', desc='an unhandled error happened while adding roles')

@main.errorhandler(404)
@main.errorhandler(401)
@main.errorhandler(400)
def generic_error(desc):
	return render_template('error.html', title='error', desc=desc)

def get_auth_url():
	with make_session() as discord:
		url, state = discord.authorization_url(DISCORD_AUTH_BASE_URL)
		session['oauth2_state'] = state
		return url

@main.route('/login')
def login():
	return redirect(get_auth_url())

@main.route('/discord')
def callback():
	state = session.get('oauth2_state')
	if not state and request.values.get('error'):
		return redirect(url_for('.index', _external=True))

	with make_session(state=state) as discord:
		token = discord.fetch_token(
			DISCORD_TOKEN_URL,
			client_secret=app.config['DISCORD_SECRET_KEY'],
			authorization_response=request.url)
		session['auth_token'] = token
		session.permanent = True
		verify_twitch()

def verify_twitch():
	username = get_twitch_name()
	if username is None:
		abort(400, 'couldn\'t find your twitch username')
	elif username == '__not_linked!':
		raise RequestRedirect(url_for('.twitch_unlinked'))
	
	following = is_following(username)
	if following is None:
		raise RequestRedirect(url_for('.twitch_error', _external=True))
	elif following is False:
		raise RequestRedirect(url_for('.follow', _external=True))

	role = add_role()
	if role is None:
		raise RequestRedirect(url_for('.discord_error', _external=True))

	session['linked'] = True
	raise RequestRedirect(url_for('.index', _external=True))