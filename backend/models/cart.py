from extensions import db
from sqlalchemy import UniqueConstraint,ForeignKey

class Cart(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    numOfProduct = db.Column(db.Integer, nullable=False)
    totalSum = db.Column(db.Integer, nullable=False)

    # unique constraint on the pair of foreign keys
    unique_constraint = UniqueConstraint('user_id','product_id',name='unique_user_product')
    # details
    user = db.relationship(
        "User",foreign_keys=[user_id]
    )
    product = db.relationship(
        "Product",foreign_keys=[product_id]
    )

    def toJson(self):
        return {
            "id": self.id,
            "user": self.user.toJson(),
            "product": self.product.toJson(),
            "numOfProduct": self.numOfProduct,
            "totalSum": self.totalSum
        }

