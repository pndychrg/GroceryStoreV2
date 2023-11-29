from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required
from lib.jobs.daily_remainder import sendMailtoUnvisitedUser
from lib.jobs.monthly_report import send_toAllUser
from lib.methods.decorators import checkJWTForAdmin
# from celery import current_app
admin = Blueprint("admin", __name__)


@admin.route("/admin/user/report", methods=['GET'])
@jwt_required()
@checkJWTForAdmin
def sendMail():
    job = send_toAllUser.apply_async()
    result = job.wait()
    print(result, flush=True)
    return "true", 200


@admin.route("/admin/user/unvisited", methods=['GET'])
@jwt_required()
@checkJWTForAdmin
def sendRemainder():
    job = sendMailtoUnvisitedUser.apply_async()
    result = job.wait()
    print(result, flush=True)
    return "true", 200
