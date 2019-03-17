from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
#from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config 	###

bootstrap = Bootstrap() 	###
db = SQLAlchemy()           ###
mail = Mail()               ###
#moment = Moment()


###create_app()		直到藍圖被app註冊時，才成為app的一部分。
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name]) 	###
    config[config_name].init_app(app)				###

    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    #moment.init_app(app)
    

    from .main import main as main_blueprint 		#連接到app/main/__init.py
    app.register_blueprint(main_blueprint)

    return app
