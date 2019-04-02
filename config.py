import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string 12345'
    ### 設置Flask-Mail來使用Gmail ###
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587')) #現在最新的標準是使用 port 587 作為安全電郵埠號
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') #郵件帳號的使用者名稱(於 Windows cmd 設定環境變數)
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') #郵件帳號的密碼(於 Windows cmd 設定環境變數)

    #主旨的開頭文字
    MAIL_SUBJECT_PREFIX = '[Flasky]'
    #寄件者的地址，同欲驗證的gmail帳號
    MAIL_SENDER = 'Flasky Admin <pcsh110576@gmail.com>'
    #收件者的地址(於 Windows cmd 設定環境變數)
    MAIL_ADMIN = os.environ.get('FLASKY_ADMIN')

    SQLALCHEMY_TRACK_MODIFICATIONS = False # 減少記憶體使用

    @staticmethod			
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql://flaskdb_chia:gibe258deny700@localhost:3306/flaskdb'
    #3306 資料庫服務的port
    #'mysql://資料庫的使用者名稱:資料庫的使用者密碼@localhost:port/資料庫名稱'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'
    #預設為【記憶體內部資料庫】，不保留資料。

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}