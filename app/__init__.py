from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

### App工廠 ### 
#create_app()		直到藍圖被app註冊時，才成為app的一部分。
def create_app(config_name):
    app = Flask(__name__) #App實例

    #將config.py內定義的Config類別，其所儲存的組態直接匯入App
    app.config.from_object(config[config_name])

    #呼叫init_app()完成App及擴充套件的初始化
    config[config_name].init_app(app)
    bootstrap.init_app(app) 
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    
    ### 註冊主藍圖 ###
    from .main import main as main_blueprint #連接到app/main/__init.py
    app.register_blueprint(main_blueprint)

    return app