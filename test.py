from flask import Flask
app = Flask(__name__)

from flask import redirect
@app.route('/')
def index():
    return redirect('http://www.example.com')