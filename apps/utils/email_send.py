# encoding: utf-8
__author__ = 'shawn'
__date__ = '2017/11/4 19:23'

from random import Random
from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from Mx_Nov.settings import DEFAULT_FROM_EMAIL


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str


def send_email(email,send_type='register'):
    code = random_str(16)
    email_record = EmailVerifyRecord()
    email_record.code = code
    email_record.email = email
    email_record.send_type =send_type
    email_record.save()

    if send_type == 'register':
        email_title = u'慕课网注册邮件'
        email_message = u'请点击 http://127.0.0.1:8000/active/{0}'.format(code)

        send_status = send_mail(email_title, email_message, DEFAULT_FROM_EMAIL, [email])
        if send_status:
            pass

    if send_type == 'forget':
        email_title = u'慕课网密码找回'
        email_message = u'请点击 http://127.0.0.1:8000/reset_pwd/{0}'.format(code)

        send_status = send_mail(email_title, email_message, DEFAULT_FROM_EMAIL, [email])
        if send_status:
            pass
