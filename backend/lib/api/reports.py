from flask import Blueprint, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required
from lib.jobs.monthly_report import send_report_asPDF
from lib.db_utils.sections import SectionDB
from lib.db_utils.products import ProductDB
from lib.methods.decorators import checkJWTForManager, checkJWTForUser
from lib.jobs.product_report import *
from cache import cache
report = Blueprint('report', __name__)
sectionDB = SectionDB()
productDB = ProductDB()


@report.route("/report/exportCSVReports", methods=['GET'])
@jwt_required()
@checkJWTForManager
# @cache.cached(timeout=30, query_string=True)
def exportCSVReports():
    job = generateCSVReports.apply_async()
    result = job.wait()
    return send_file(result, as_attachment=True), 200


@report.route("/report/coupon", methods=['GET'])
@jwt_required()
@checkJWTForManager
# @cache.cached(timeout=30, query_string=True)
def getCouponEngGraph():
    job = generateCouponEngBarGraph.apply_async()
    result = job.wait()
    return send_file(result, mimetype='image/png', as_attachment=True, download_name='coupon_usage.png')


@report.route("/report/product/favourite", methods=['GET'])
@jwt_required()
@checkJWTForManager
# @cache.cached(timeout=30, query_string=True)
def getFavProductGraph():
    job = generateFavProductGraph.apply_async()
    img_path = job.wait()
    return send_file(img_path, mimetype='image/png', as_attachment=True, download_name='fav_product.png')


@report.route('/report/product/buy', methods=['GET'])
@jwt_required()
@checkJWTForManager
# @cache.cached(timeout=30, query_string=True)
def getProductBoughtGraph():
    job = generateProductEngBarGraph.apply_async()
    img_path = job.wait()
    return send_file(img_path, mimetype='image/png', as_attachment=True, download_name='fav_product.png')


@report.route('/report/data', methods=['GET'])
@jwt_required()
@checkJWTForManager
@cache.cached(timeout=30, query_string=True)
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


@report.route('/report/user/pdf', methods=['GET'])
@jwt_required()
@checkJWTForUser
def getUserReportAsPDF():
    # getting the user_id from the jwt
    # user = get_jwt_identity()
    user_id = get_jwt_identity().get('id')
    # print(user_id)
    job = send_report_asPDF.apply_async(args=[user_id])
    pdf_path = job.wait()
    # print(pdf_path, flush=True)
    return send_file(pdf_path, mimetype="application/pdf", as_attachment=True, download_name="month_report.pdf")


# @report.route('/report/user/data',methods=)
