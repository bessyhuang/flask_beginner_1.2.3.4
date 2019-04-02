### mariadb 連接 db_demo.py 與 webform.html ###

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate #用Flask-Migrate進行資料庫遷移


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import session, redirect, url_for

from flask import render_template
from flask_bootstrap import Bootstrap

from flask import flash
from flask_moment import Moment
from datetime import datetime

import os
from flask_mail import Mail
from flask_mail import Message
from threading import Thread

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flaskdb_chia:gibe258deny700@localhost:3306/flaskdb'
#3306 資料庫服務的port
#'mysql://資料庫的使用者名稱:資料庫的使用者密碼@localhost:port/資料庫名稱'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 減少記憶體使用

app.config['SECRET_KEY'] = 'hard to guess string 12345'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

app.config['MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['MAIL_SENDER'] = 'Flasky Admin <pcsh110576@gmail.com>'
app.config['MAIL_ADMIN'] = os.environ.get('FLASKY_ADMIN')

def send_email(to, subject, template, **kwargs):
	msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject, sender = app.config['MAIL_SENDER'], recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	#msg.html = render_template(template + '.html', **kwargs)
	thr = Thread(target=send_async_email, args=[app, msg])
	thr.start()
	return thr

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

db = SQLAlchemy(app)
migrate = Migrate(app, db) #用Flask-Migrate進行資料庫遷移

bootstrap = Bootstrap(app)
moment = Moment(app)

mail = Mail(app)


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

class NameForm(FlaskForm):
    name = StringField('what is your name?', validators=[DataRequired()] )
    submit = SubmitField('Submit')


@app.route('/name_form', methods=['GET', 'POST'])
def name_form():
    form = NameForm()
    if form.validate_on_submit():
        # 用表單收到的name在資料庫中查詢
        user = User.query.filter_by(username=form.name.data).first()

        # 查無此姓名的話，將該姓名寫入資料庫
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if app.config['MAIL_ADMIN']: ###
                send_email(app.config['MAIL_ADMIN'], 'New User', 'mail/new_user', user=user) ###
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''

        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        
        return redirect(url_for('name_form'))
    return render_template('webform.html', form=form, name=session.get('name'), current_time=datetime.utcnow(), known=session.get('known', False))