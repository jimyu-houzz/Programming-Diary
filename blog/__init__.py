from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from blog.config import Config


# Create instances of flask objects to be used in other files
# Don't put "app" in these instances yet, put them in the "create_app" function

db = SQLAlchemy()
# create Bcrypt instance, encrypt user password
bcrypt = Bcrypt()

# create LoginManager instance
login_manager = LoginManager()
# force user to login if trying to go to unauthenticated routes
login_manager.login_view = 'users.login' # function name
# bootstrap class to style the message
login_manager.login_message_category = 'info' 
mail = Mail()

# function to create the whole app with multiple packages
# using the CONFIG class from config.py
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # put the "app" here
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from blog.users.routes import users
    from blog.posts.routes import posts
    from blog.main.routes import main
    # different import ways for error handlers
    from blog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app