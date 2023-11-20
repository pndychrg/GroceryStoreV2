import csv
from datetime import datetime
import zipfile
from sqlalchemy import extract
from models.products import Product
from models.order import Order
from models.bill import Bill
from models.coupon import Coupon
from models.section import Section
from extensions import db


def exportProductReportToCSV():
    # this funciton will create csv files

    # querying the database to fetch all the data at once
    orders = Order.query.all()
    products = Product.query.all()
    last_month = datetime.today().month - 1
    bills = Bill.query.filter(extract('year', Bill.date) == datetime.today(
    ).year, extract('month', Bill.date == last_month)).all()
    # coupons = Coupon.query.all()
    sections = Section.query.all()
    section_filename = "static/export/section.csv"
    with open(section_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(
            ['ID', "Section Name", "Unit", "Number of Products"])
        # writing the data
        for section in sections:
            csv_writer.writerow(
                [section.id, section.name, section.unit, len(section.products)]
            )

    # creating a coupon file
    coupon_filename = "static/export/coupons.csv"
    # counting the coupon_usage
    coupon_usage = db.session.query(
        Coupon.id,
        Coupon.coupon_code,
        Coupon.discount,
        Coupon.expiryDate,
        Coupon.hasExpired,
        db.func.count(Bill.coupon_id).label('usage_count')
    ).join(Bill).group_by(Coupon.coupon_code).all()
    # print("Coupon Usage",coupon_usage)
    with open(coupon_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(
            ['ID', 'Coupon Code', 'Discount',
                'ExpiryDate', 'HasExpired', 'Usage Count']
        )
        for coupon in coupon_usage:
            csv_writer.writerow(coupon)

    # creating a products file
    product_fileName = "static/export/products.csv"
    product_details = db.session.query(
        Product.id,
        Product.name,
        Product.description,
        Product.rate,
        Product.avg_rating,
        Product.availableAmount,
        Product.manufactureDate,
        Product.expiryDate,
        Section.name,
        Section.unit,
        db.func.count(Order.product_id).label("bought_by_user_count")
    ).join(Section, Section.id == Product.section_id).join(Order).group_by(Product.id).all()
    # print(product_details)
    with open(product_fileName, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(
            [
                'ID', 'NAME', 'DESCRIPTION', 'RATE', 'AVG_RATING', 'AVAILABLE_AMOUNT', 'MANUFACTURE_DATE', 'EXPIRY_DATE', 'SECTION NAME', 'SECTION UNIT', 'BOUGHT BY USER'
            ]
        ),
        for product in product_details:
            csv_writer.writerow(
                product
            )

    # revenue file containing bill details , and total revenue that was generated in previous month
    revenue_fileName = "static/export/revenue.csv"
    total_revenue = 0
    # iterating the bills
    # for bill in bills:
    #     total_revenue += bill.finalAmount
    with open(revenue_fileName, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(
            ['BILL ID', 'DATE', 'BILL AMOUNT']
        )
        for bill in bills:
            total_revenue += bill.finalAmount
            csv_writer.writerow(
                [bill.id, datetime.strftime(
                    bill.date, "%Y-%m-%d"), bill.finalAmount]
            )
        csv_writer.writerow([])
        csv_writer.writerow(["TOTAL REVENUE", total_revenue])

    # now creating the zip file
    # create a zip file containing the csv files
    zip_filename = 'static/export/data.zip'
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(section_filename, arcname='section.csv')
        zipf.write(product_fileName, arcname='products.csv')
        zipf.write(coupon_filename, arcname='coupons.csv')
        zipf.write(revenue_fileName, arcname='revenue.csv')
    return zip_filename
