from flask import Blueprint, send_file
from flask_jwt_extended import jwt_required
from lib.jobs.monthly_report import send_report_asPDF
from lib.db_utils.sections import SectionDB
from lib.db_utils.products import ProductDB
from lib.methods.decorators import checkJWTForManager, checkJWTForUser
from lib.jobs.product_report import *
report = Blueprint('report', __name__)
sectionDB = SectionDB()
productDB = ProductDB()


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
    job = generateCouponEngBarGraph.apply_async()
    result = job.wait()
    return send_file(result, mimetype='image/png', as_attachment=True, download_name='coupon_usage.png')


@jwt_required()
@checkJWTForManager
@report.route("/report/product/favourite", methods=['GET'])
def getFavProductGraph():
    job = generateFavProductGraph.apply_async()
    img_path = job.wait()
    return send_file(img_path, mimetype='image/png', as_attachment=True, download_name='fav_product.png')


@jwt_required()
@checkJWTForManager
@report.route('/report/product/buy', methods=['GET'])
def getProductBoughtGraph():
    job = generateProductEngBarGraph.apply_async()
    img_path = job.wait()
    return send_file(img_path, mimetype='image/png', as_attachment=True, download_name='fav_product.png')


@jwt_required()
@checkJWTForManager
@report.route('/report/data', methods=['GET'])
def getMonthRevenue():
    revenue = totalRevenueMonth()
    sections = [section.toJson() for section in sectionDB.getEmptySections()]
    products = [product.toJson()
                for product in productDB.getUnavailableProduct()]
    return {
        "revenue": revenue,
        "sections": sections,
        "products": products
    }, 200


@jwt_required()
@checkJWTForUser
@report.route('/report/user', methods=['GET'])
def getUserReportAsPDF():
    job = send_report_asPDF.apply_async()
    pdf_path = job.wait()
    print(pdf_path, flush=True)
    return send_file(pdf_path, mimetype="application/pdf", as_attachment=True, download_name="month_report.pdf")
