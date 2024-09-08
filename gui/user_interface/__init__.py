from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import CSRFProtect
from flask_mail import Mail

from gui.user_interface.config import config_by_name


db = SQLAlchemy()

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"

toolbar = DebugToolbarExtension()
mail = Mail()

# for displaying timestamps
moment = Moment()

primary_users = {'utibe47@gmail.com'}


def create_app(config_name):
    app = Flask(__name__)
    _config = config_by_name[config_name]
    app.config.from_object(_config)
    bootstrap = Bootstrap(app)

    app.threaded = True
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from .authorization import authorization as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    CSRFProtect(app)

    return app
