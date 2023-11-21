from workers import celery
from lib.methods.product_csv import exportProductReportToCSV


@celery.task()
def generateCSVReports():
    zipFile = exportProductReportToCSV()
    return zipFile
