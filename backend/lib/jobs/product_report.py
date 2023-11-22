from workers import celery
from lib.methods.product_csv import exportProductReportToCSV
from lib.methods.engagement_graphs import *


@celery.task()
def generateCSVReports():
    zipFile = exportProductReportToCSV()
    return zipFile


@celery.task()
def generateCouponEngBarGraph():
    img_path = couponEngBarGraph()
    return img_path


@celery.task()
def generateFavProductGraph():
    img_path = mostFavProductGraph()
    return img_path


@celery.task()
def generateProductEngBarGraph():
    img_path = productEngBarGraph()
    return img_path


# @celery.task()
# def generateTotalRevenueMonth():
#     revenue = totalRevenueMonth()
#     return revenue
