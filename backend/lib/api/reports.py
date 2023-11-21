from flask import Blueprint, send_file
from flask_jwt_extended import jwt_required
from lib.methods.decorators import checkJWTForManager
from lib.methods.engagement_graphs import *
from lib.jobs.product_report import generateCSVReports
report = Blueprint('report', __name__)


@jwt_required()
@checkJWTForManager
@report.route("/report/exportCSVReports", methods=['GET'])
def exportCSVReports():
    job = generateCSVReports.apply_async()
    result = job.wait()
    return send_file(result, as_attachment=True), 200


@jwt_required()
@checkJWTForManager
@report.route("/report/coupon", methods=['GET'])
def getCouponEngGraph():
    img_path = couponEngBarGraph()
    return send_file(img_path, mimetype='image/png', as_attachment=True, download_name='coupon_usage.png')


@jwt_required()
@checkJWTForManager
@report.route("/report/product/favourite", methods=['GET'])
def getFavProductGraph():
    img_path = mostFavProductGraph()
    return send_file(img_path, mimetype='image/png', as_attachment=True, download_name='fav_product.png')


@jwt_required()
@checkJWTForManager
@report.route('/report/product/buy', methods=['GET'])
def getProductBoughtGraph():
    img_path = productEngBarGraph()
    return send_file(img_path, mimetype='image/png', as_attachment=True, download_name='fav_product.png')


@jwt_required()
@checkJWTForManager
@report.route('/report/data/revenue', methods=['GET'])
def getMonthRevenue():
    revenue = totalRevenueMonth()
    return str(revenue), 200
