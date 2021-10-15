import os
from flask import Flask
from blogpost.config import config
from blogpost.core.views import core
from blogpost.error_pages.handlers import error_pages

app = Flask(__name__)

flask_env = os.environ.get('FLASK_ENV') or 'default'

app.config.from_object(config[flask_env])

app.register_blueprint(core)
app.register_blueprint(error_pages)
