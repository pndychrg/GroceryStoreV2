from celery import group
from workers import celery
from jinja2 import Template
from lib.methods.mail import send_email
from lib.db_utils.user_db import UserDB
import pdfkit
userDB = UserDB()


@celery.task()
def send_user_monthly_report(user_id):
    data = userDB.getPreviousMonthUserData(user_id=user_id)
    # print(print([bill.toJson() for bill in data['bills']], flush=True))
    with open("../backend/static/docs/user_montly_report.html") as file:
        template = Template(file.read())
        message = template.render(data=data)

    response = send_email(data['user'].email, subject="hello", message=message)
    return response


@celery.task()
def send_toAllUser():
    user_list = userDB.getAllUser()
    res = group(send_user_monthly_report.s(user.id) for user in user_list)()
    return res


@celery.task()
def send_user_current_month_report():
    data = userDB.getUserCurrentMonthData(3)
    with open("../backend/static/docs/user_montly_report.html") as file:
        template = Template(file.read())
        message = template.render(data=data)

    response = send_email(data['user'].email, subject="hello", message=message)
    return response


@celery.task()
def send_report_asPDF(user_id):
    if user_id == None:
        return None
    data = userDB.getUserCurrentMonthData(user_id)
    # print(data['img'])
    # print(data)
    with open("../backend/static/docs/user_montly_report.html") as file:
        template = Template(file.read())
        message = template.render(data=data)
    pdf_content = pdfkit.from_string(message)
    pdf_filename = "static/export/report.pdf"

    with open(pdf_filename, 'wb') as pdf_file:
        pdf_file.write(pdf_content)

    # print(pdf_filename)
    return pdf_filename
