from flask import Flask, render_template
from flask_bootstrap import Bootstrap 	### 繼承 bootstrap 模板
from flask_moment import Moment 	### 初始化 flask_moment

from datetime import datetime 	###添加datetime變數

app = Flask(__name__)
bootstrap = Bootstrap(app) 	### 繼承 bootstrap 模板
moment = Moment(app) 	### 初始化 flask_moment

### 繼承 自訂模板

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

### 繼承 bootstrap 模板

@app.route('/index2')
def index2():
    return render_template('index2.html', current_time=datetime.utcnow())

@app.route('/user2/<name>')
def user2(name):
    return render_template('user2.html', name=name)



