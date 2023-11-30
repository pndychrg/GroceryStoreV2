from workers import celery
from jinja2 import Template
from lib.methods.mail import send_email


@celery.task()
def send_updated_password_mail(data):
    with open("../backend/static/docs/password_update.html") as file:
        template = Template(file.read())
        message = template.render(data=data)

    response = send_email(data['user'].get('email'),
                          subject="Forgot Password", message=message)
    return True
