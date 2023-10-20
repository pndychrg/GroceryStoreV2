from extensions import db


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey("bill.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    numOfProduct = db.Column(db.Integer, nullable=False)
    totalSum = db.Column(db.Integer, nullable=False)

    # details
    product = db.relationship(
        "Product",foreign_keys=[product_id]
    )

    def toJson(self):
        return {
            "id":self.id,
            "product":self.product.toJson(),
            "numOfProduct":self.numOfProduct,
            "totalSum":self.totalSum
        }
    
    