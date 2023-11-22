from extensions import db


class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coupon_code = db.Column(db.String(10), nullable=False, unique=True)
    discount = db.Column(db.Integer)
    expiryDate = db.Column(db.DateTime)
    hasExpired = db.Column(db.Integer, default=0)

    def toJson(self):
        return {
            "id": self.id,
            "coupon_code": self.coupon_code,
            "discount": self.discount,
            "expiryDate": self.expiryDate.strftime('%Y-%m-%d') if self.expiryDate != None else None,
            "hasExpired": self.hasExpired
        }
