from workers import celery
from datetime import datetime
from celery.schedules import crontab
from jinja2 import Template
from lib.methods.mail import send_email
from lib.db_utils.user_db import UserDB

userDB = UserDB()


@celery.task()
def send_user_monthly_report():
    data = userDB.getUserData(1)
    print(data)
    with open("../backend/static/docs/user_montly_report.html") as file:
        template = Template(file.read())
        message = template.render(data=data)

    response = send_email(data['user'].email, subject="hello", message=message)
    return response


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        30.0, send_user_monthly_report.s(), name="At Every 10 secs")
