from celery import group
from lib.methods.mail import send_email
from lib.db_utils.products import ProductDB
from workers import celery
from lib.db_utils.user_db import UserRemainder
from jinja2 import Template
userRemainder = UserRemainder()
productDB = ProductDB()


@celery.task()
def sendMailtoUnvisitedUser():
    users = userRemainder.getNonVisitedUsers()
    latestProduct = productDB.getMostRecentProducts(1)[0]
    highestRatedProduct = productDB.getHighestRatedProduct()
    mostLikedProduct = productDB.getMostFavouredProduct()

    for user in users:
        data = {
            "user": user,
            "latestProduct": latestProduct,
            "highestRatedProduct": highestRatedProduct,
            "mostLikedProduct": mostLikedProduct,
        }

        with open("../backend/static/docs/user_remainder.html") as file:
            template = Template(file.read())
            message = template.render(data=data)

            response = send_email(
                data['user'].email, subject="Remainder to visit", message=message)

            print(
                f"Sent Remainder to user {data['user'].username} : {response}")
    # print([user.toJson() for user in users])

    return True
