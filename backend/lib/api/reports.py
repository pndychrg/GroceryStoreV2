from flask import Blueprint,send_file
from flask_jwt_extended import jwt_required
from lib.methods.decorators import checkJWTForManager
from lib.jobs.product_report import generateCSVReports
report = Blueprint('report',__name__)

@jwt_required()
@checkJWTForManager
@report.route("/report/exportCSVReports",methods=['GET'])
def exportCSVReports():
    job = generateCSVReports.apply_async()
    result = job.wait()
    return send_file(result,as_attachment=True),200
