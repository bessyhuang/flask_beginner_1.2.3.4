from flask import Flask, render_template
from flask_bootstrap import Bootstrap 	

### 定義表單類別
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask import session, redirect, url_for

from flask import flash

app = Flask(__name__) 	### 設置Flask-WTF
app.config['SECRET_KEY'] = 'hard to guess string 12345' 	### 設置Flask-WTF

bootstrap = Bootstrap(app) 	

class NameForm(FlaskForm):
	name = StringField('What is your name?', validators=[DataRequired()])
	submit = SubmitField('Submit')

@app.route('/webform', methods=['GET', 'POST'])
def webform():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('webform.html', form=form, name=name)

@app.route('/webform2', methods=['GET', 'POST'])
def webform2():
    name2 = None
    form = NameForm()
    if form.validate_on_submit():
        name2 = form.name.data
        form.name.data = ''
    return render_template('webform2.html', form=form, name=name2)

@app.route('/webform3', methods=['GET', 'POST'])
def webform3():
    #name = None
    form = NameForm()
    if form.validate_on_submit():
    	session['name'] = form.name.data
    	return redirect(url_for('webform3')) #def
        #name3 = form.name.data
        #form.name.data = ''
    return render_template('webform3.html', form=form, name=session.get('name')) #

@app.route('/webform4', methods=['GET', 'POST'])
def webform4():

    form = NameForm()
    if form.validate_on_submit():
    	old_name = session.get('name')
    	if old_name is not None and old_name != form.name.data:
    		flash('Looks like tou have changed your name!')
    	session['name'] = form.name.data

    	return redirect(url_for('webform4')) #def
    return render_template('webform4.html', form=form, name=session.get('name')) #