from flask_mail import Message
# from app import create_app
from flask import current_app,render_template
from app.extensions import mail
#封装函数  发送邮件
"""
@:param to  发送给谁 
@:param subject  邮件主题 
@:param 内容   网页邮件  还有手机电脑客户端邮件 
@:param 其它参数  
"""


def send_mail(to, subject, template, **kwargs):
    # app = create_app('development')
    app = current_app._get_current_object()
    msg = Message(subject=subject, recipients=[to], sender=app.config['MAIL_USERNAME'])

    #浏览器端显示的内容
    msg.html = render_template(template+'.html', **kwargs)

    #客户端显示的内容
    msg.body = render_template(template + '.txt', **kwargs)
    #发送邮件   邮件对象.send
    mail.send(message=msg)


