import os
from flask import Flask
from flask_migrate import Migrate
from blogpost.db import db
from blogpost.login_manager import login_manager
from blogpost.config import config
from blogpost.core.views import core
from blogpost.error_pages.handlers import error_pages

app = Flask(__name__)

# ENV Config
flask_env = os.environ.get('FLASK_ENV') or 'default'
app.config.from_object(config[flask_env])

# db Setup
db.init_app(app)
Migrate(app, db)


# Login Config
login_manager.init_app(app)
login_manager.login_view = 'users.login'


app.register_blueprint(core)
app.register_blueprint(error_pages)
