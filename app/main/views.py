from datetime import datetime
from flask import flash
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User

from flask import current_app
from ..email import send_email

@main.route('/name_form', methods=['GET', 'POST'])
def name_form():
    form = NameForm()
    if form.validate_on_submit():
        # 用表單收到的name在資料庫中查詢
        user = User.query.filter_by(username=form.name.data).first()

        # 查無此姓名的話，將該姓名寫入資料庫
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit() #把表單所輸入的，寫進資料庫
            session['known'] = False
            if current_app.config['MAIL_ADMIN']:
                send_email(current_app.config['MAIL_ADMIN'], 'New User', 'mail/new_user', user=user) 	###
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''

        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        
        return redirect(url_for('main.name_form')) #return redirect(url_for('.name_form'))
    return render_template('webform.html', form=form, name=session.get('name'), current_time=datetime.utcnow(), known=session.get('known', False))