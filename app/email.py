#當你要同時做很多事情時，就可以用到threading達成多執行緒。
from threading import Thread
from flask_mail import Message
from flask import current_app, render_template
from . import mail

#send_email(收件人地址, 主旨, email內文模板, 關鍵字引數)
def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()

    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject, sender = app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    #msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
