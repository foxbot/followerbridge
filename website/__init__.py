from flask import Flask
import os

from . import views

def create_app(conf):
	app = Flask(__name__)
	app.config.from_object(conf)

	# for testing env
	if 'http://' in app.config['REDIRECT_URI']:
		os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

	app.register_blueprint(views.main)
	return app