import os
from flask import Flask
from flask_migrate import Migrate
from blogpost.db import db
from blogpost.login_manager import login_manager
from blogpost.config import config
from blogpost.core.views import core
from blogpost.users.views import users
from blogpost.blog_posts.views import blog_posts
from blogpost.error_pages.handlers import error_pages
from flask_simplemde import SimpleMDE
from flaskext.markdown import Markdown

app = Flask(__name__)

# ENV Config
flask_env = os.environ.get('FLASK_ENV') or 'default'
app.config.from_object(config[flask_env])

# db Setup
db.init_app(app)
Migrate(app, db)

app.config['SIMPLEMDE_JS_IIFE'] = True
app.config['SIMPLEMDE_USE_CDN'] = True
SimpleMDE(app)
Markdown(app, extensions=['fenced_code', 'tables'])

# Login Config
login_manager.init_app(app)
login_manager.login_view = 'users.login'


app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(error_pages)
