from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import session, redirect, url_for

from flask import render_template
from flask_bootstrap import Bootstrap

from flask import flash
from flask_moment import Moment
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string 12345'
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
	name = StringField('what is your name?', validators=[DataRequired()] )
	submit = SubmitField('Submit')
	

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data

        return redirect(url_for('index'))
    return render_template('webform.html', form=form, name=session.get('name'), current_time=datetime.utcnow())
