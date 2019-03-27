### mariadb 連接 db_demo.py 與 flask shell 操作 --- 尚未連結 webform.html ###

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate #用Flask-Migrate進行資料庫遷移

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flask_demo:GIBE258DENY700@localhost:3306/flask_db'
#3306 資料庫服務的port
#'mysql://資料庫的使用者名稱:資料庫的使用者密碼@localhost:port/資料庫名稱'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 減少記憶體使用

db = SQLAlchemy(app)

migrate = Migrate(app, db) #用Flask-Migrate進行資料庫遷移

class Role(db.Model):
    __tablename__ = 'roles' # 建立Table名稱
    id = db.Column(db.Integer, primary_key=True) # 建立id欄位，整數型態，primary key
    name = db.Column(db.String(64), unique=True) # 建立name欄位, 變數型態(長度64), 值不可重複 unique=True
    users = db.relationship('User', backref='role') # 建立反向參考

    def __repr__(self):
        return "<Role %r>" % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True) #建立索引，方便查詢 index=True
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id')) 

    def __repr__(self):
        return "<User %r>" % self.username

#關聯式資料庫：省空間&方便修改
