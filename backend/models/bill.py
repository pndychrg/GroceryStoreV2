from extensions import db


class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    billAmount = db.Column(db.Integer, nullable=False,)
    coupon_id = db.Column(db.Integer, db.ForeignKey("coupon.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.DateTime)
    finalAmount = db.Column(db.Integer)
    coupon = db.relationship("Coupon", backref="bill",
                             foreign_keys=[coupon_id])
    orders = db.relationship("Order", backref="bill")

    def toJson(self):
        return {
            "id": self.id,
            "orders": [order.toJson() for order in self.orders],
            "date": self.date.strftime('%Y-%m-%d') if self.date != None else None,
            "finalAmount": self.finalAmount,
            "billAmount": self.billAmount,
            "coupon": self.coupon.toJson() if self.coupon else None,
        }
