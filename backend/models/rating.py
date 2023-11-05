from extensions import db


class Rating(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        "product.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String())

    #
    product = db.relationship("Product", foreign_keys=[product_id])
    user = db.relationship("User", foreign_keys=[user_id])

    def toJson(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "rating": self.rating,
            "comment": self.comment,
        }
