from flask import Flask, render_template
from flask_bootstrap import Bootstrap 	
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import session, redirect, url_for

import os
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Message
from threading import Thread

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__) 	### 設置Flask-WTF
app.config['SECRET_KEY'] = 'hard to guess string 12345' 	### 設置Flask-WTF

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#主旨的開頭文字
app.config['MAIL_SUBJECT_PREFIX'] = '[Flasky]'
#寄件者的地址，同欲驗證的gmail帳號
app.config['MAIL_SENDER'] = 'Flasky Admin <pcsh110576@gmail.com>'
#收件者
app.config['MAIL_ADMIN'] = os.environ.get('FLASKY_ADMIN')


bootstrap = Bootstrap(app) 	
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

class NameForm(FlaskForm):
	name = StringField('What is your name?', validators=[DataRequired()])
	submit = SubmitField('Submit')

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), unique = True)
	users = db.relationship('User', backref='role', lazy='dynamic')

	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), unique = True, index = True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username

def send_email(to, subject, template, **kwargs):
	msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject, sender = app.config['MAIL_SENDER'], recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	thr = Thread(target=send_async_email, args=[app, msg])
	thr.start()
	return thr

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if app.config['MAIL_ADMIN']: ###新增
                send_email(app.config['MAIL_ADMIN'], 'New User', 'mail/new_user', user=user) ###新增
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('webform.html', form=form, name=session.get('name'), known=session.get('known', False))
