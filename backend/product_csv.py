import csv
from models.products import Product
from models.order import Order
from models.bill import Bill
from models.coupon import Coupon
from models.section import Section
from extensions import db
from run import app


def exportProductReportToCSV():
    # this funciton will create csv files

    # querying the database to fetch all the data at once
    orders = Order.query.all()
    products = Product.query.all()
    # coupons = Coupon.query.all()
    sections = Section.query.all()
    section_filename = "backend/static/export/section.csv"
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
    coupon_filename = "backend/static/export/coupons.csv"
    # counting the coupon_usage
    coupon_usage = db.session.query(
        Coupon.coupon_code,
        db.func.count(Bill.coupon_id).label('usage_count')
    ).join(Bill).group_by(Coupon.coupon_code).all()
    print("Coupon Usage",coupon_usage)
    with open(coupon_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(
            ['ID', 'Coupon Code', 'Discount', 'ExpiryDate', 'HasExpired']
        )


if __name__ == "__main__":
    with app.app_context():
        exportProductReportToCSV()
