from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import abort

app = Flask(__name__)

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '''<h1>Hello World!</h1><br>
            <p>Your browser is {}</p>'''.format(user_agent)

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)

@app.route('/cookie')
def cookie():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer','42')
    return response

@app.route('/redirect') ##
def redirect():
    return redirect(url_for('/'))

@app.route('/test/<id>') ##
def test(id):
    test = load_user(id)
    if not test:
        abort(404)
    return '<h1>Hello, {}!</h1>'.format(test.name)
