from . import db

class Role(db.Model):
    __tablename__ = 'roles' # 建立Table名稱
    id = db.Column(db.Integer, primary_key=True) # 建立id欄位，整數型態，primary key
    name = db.Column(db.String(64), unique=True) # 建立name欄位, 變數型態(長度64), 值不可重複 unique=True
    users = db.relationship('User', backref='role', lazy='dynamic') # 建立反向參考

    def __repr__(self):
        return "<Role %r>" % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True) #建立索引，方便查詢 index=True
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def __repr__(self):
        return "<User %r>" % self.username

#關聯式資料庫：省空間&方便修改