import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import extract
from models.order import Order
from models.favourites import Favourites
from models.products import Product
# from models.section import Section
from models.bill import Bill
from datetime import datetime
from models.coupon import Coupon
from extensions import db
import matplotlib

matplotlib.use('Agg')

# to remove runtime error


def couponEngBarGraph():
    coupon_usage = db.session.query(
        Coupon.coupon_code,
        db.func.count(Bill.coupon_id).label("usage_count")
    ).join(Bill).group_by(Coupon.coupon_code).all()

    coupon_codes = [usage[0] for usage in coupon_usage]
    # print(coupon_codes)
    usage_count = [usage[1] for usage in coupon_usage]

    plt.bar(coupon_codes, usage_count)
    plt.xlabel('Coupon Code')
    plt.ylabel("Frequency")
    plt.title("Frequency of Coupon Usage In Bills")
    plt.tight_layout()

    # save the bar graph as img file in static folder
    img_path = 'static/img/coupon_usage.png'
    plt.savefig(img_path, format='png')
    plt.close()

    return img_path

# creating favourites Graph


def mostFavProductGraph():
    # getting the data from backend

    fav_products = db.session.query(
        Product.name,
        db.func.count(Favourites.product_id).label("Wishlisted_by_userCount")).join(Favourites).group_by(Product.id).all()

    # making data lists
    favProductName = []
    favProductCount = []

    for product in fav_products:
        favProductName.append(product[0])
        favProductCount.append(product[1])

    plt.bar(favProductName, favProductCount)
    plt.xlabel("Proudct Name")
    plt.ylabel("Frequency")
    plt.title("Frequncy of Product in User's Favourites List")
    plt.tight_layout()

    # saving the bar graph
    img_path = 'static/img/fav_product.png'
    plt.savefig(img_path, format='png')
    plt.close()

    return img_path


def productEngBarGraph():

    try:
        products_bought_data = db.session.query(
            Product.id,
            Product.name,
            db.func.sum(Order.numOfProduct).label('frequency')
        ).join(Order, Product.id == Order.product_id).group_by(Product.id).order_by(db.desc('frequency')).all()

        # plotting
        df = pd.DataFrame(products_bought_data, columns=[
                          'Product ID', 'Product Name', 'Frequency'])

        plt.figure()
        plt.bar(df['Product Name'], df['Frequency'])
        plt.xlabel('Product Name')
        plt.ylabel('Frequency')
        plt.title('Products Bought Frequency')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # saving the img
        img_path = 'static/img/products_bought.png'
        plt.savefig(img_path, format='png')
        # closing the plot
        plt.close()

        return img_path

    except Exception as e:
        print(str(e))
        return None


def totalRevenueMonth():

    # creating this month datetime
    today = datetime.today()
    # fetching all the bills for this month
    bills = Bill.query.filter(extract('year', Bill.date) == today.year, extract(
        'month', Bill.date) == today.month)

    # calculating total revenue and products sold
    totalRevenue = 0
    # totalProductsSold = 0

    for bill in bills:
        totalRevenue += bill.finalAmount

    return totalRevenue
