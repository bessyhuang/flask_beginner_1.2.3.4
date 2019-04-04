### app/__init__.py：App套件建構式 ###

##匯入多數目前正在使用的Flask擴充套件
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
#匯入config.py
from config import config

#尚未初始化
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

### App工廠 ### 
##create_app()為"App工廠函式"，回傳建立好的App實例。直到藍圖被app註冊時，才成為app的一部分。
def create_app(config_name):  #config_name接收組態名稱，以讓App使用
    #建立App實例
    app = Flask(__name__)

    #將config.py內定義的組態類別，其所儲存的組態設定直接匯入App
    app.config.from_object(config[config_name])

    #App初始化，使用init_app()
    config[config_name].init_app(app)
    bootstrap.init_app(app) 
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    
    ### 註冊主藍圖 ###
    # 在這裡指派"路由"與"錯誤頁面處理函式" #
    # 直到藍圖被app註冊時，才成為app的一部分。
    from .main import main as main_blueprint #連接到app/main/__init.py
    app.register_blueprint(main_blueprint)

    return app
