from flask import Flask, render_template
from simpledu.config import configs
from simpledu.models import db, Course, User
from flask_migrate import Migrate
from flask_login import LoginManager

def create_app(config):
    """ 可以根据传入的 config 名称，加载不同的配置
    """
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    register_extensions(app)
    register_blueprint(app)
    return app

def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'

def register_blueprint(app):
    from .handlers import front, course, admin, user, live
    app.register_blueprint(front)
    app.register_blueprint(course)
    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(live)
