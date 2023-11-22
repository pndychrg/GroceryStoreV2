from workers import celery
from lib.db_utils.coupons import CouponDB

couponDB = CouponDB()


@celery.task()
def updateCoupons():
    print("Coupon Expiration Updated")
    couponDB.updateExpirationValue()
