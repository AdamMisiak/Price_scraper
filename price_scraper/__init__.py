import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'

# mail settings
app.config.update(dict(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='test.flask369@gmail.com',
    MAIL_PASSWORD='Testflask369'
))

# mail accounts
app.config['MAIL_DEFAULT_SENDER'] = 'test.flask369@gmail.com'

db = SQLAlchemy(app)
migrate = Migrate(app,db)
mail = Mail(app)


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return None
login_manager.login_view = "users.login"


from price_scraper.assets.views import assets_blueprint
from price_scraper.users.views import users_blueprint

app.register_blueprint(assets_blueprint,url_prefix='/assets')
app.register_blueprint(users_blueprint,url_prefix='/users')
