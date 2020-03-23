from django.core.mail import send_mail
from django.template import loader


def send_email(name,email,token):
    subject = '英雄联盟'
    message = ''

    context = {
        'name': name,
        'url': 'http://127.0.0.1:8000/axfuser/checkemail/?token='+str(token)
    }
    hm = loader.get_template('axf/user/register/email.html').render(context=context)

    html_message = hm
    from_email = 'ww_jie98@163.com'
    recipient_list = [email]

    send_mail(subject=subject,
              message=message,
              html_message=html_message,
              from_email=from_email,
              recipient_list=recipient_list)
