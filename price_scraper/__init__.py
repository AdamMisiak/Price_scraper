import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

# CREATING FLASK APP
app = Flask(__name__)

# CREATING DB URI
basedir = os.path.abspath(os.path.dirname(__file__))
database_uri = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

# APP DEVELOPMENT CONFIGURATION
app.config.from_object("config.DevelopmentConfig")

# CREATING DB AND FLASK MAIL
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

# INITIALIZING LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
	return None


login_manager.login_view = "users.login"

# ADDING BLUEPRINTS
from price_scraper.assets.views import assets_blueprint
from price_scraper.users.views import users_blueprint

app.register_blueprint(assets_blueprint, url_prefix='/assets')
app.register_blueprint(users_blueprint, url_prefix='/users')


#coverage (chyba nowa linijka od matti z xlm)
#docker compose