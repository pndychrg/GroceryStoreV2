from models.rating import Rating
from extensions import db
from lib.methods.validators import Validators
from lib.db_utils.products import ProductDB


class RatingMethods:

    def getProductRatingForUser(self, user_id, product_id):
        rating = Rating.query.filter_by(
            user_id=user_id, product_id=product_id).first()
        if rating:
            return rating, "Rating Found"
        else:
            return None, "Rating not found"

    def rateProduct(self, user_id, product_id, rating, comment):
        # checking if user already rated the product:
        existingRating, msg = self.getProductRatingForUser(
            user_id=user_id, product_id=product_id)
        if existingRating:
            existingRating.rating = rating
            existingRating.comment = comment
            db.session.commit()
            return existingRating, "Rating updated"
        # if user has not already rated the product then create a new rating value
        else:
            newRating = Rating(
                user_id=user_id, product_id=product_id, rating=rating, comment=comment)
            db.session.add(newRating)
            db.session.commit()

            return newRating, "Product Rated"

    def getAllRatingsForProduct(self, product_id):
        productRatings = Rating.query.filter_by(product_id=product_id).all()
        return productRatings

    def updateAvgRatingForProduct(self, product_id):
        # fetchinig all the product ratings
        productRatings = self.getAllRatingsForProduct()
        # calculating the avg

    def deleteRating(self, user_id, product_id):
        existingRating, msg = self.getProductRatingForUser(
            user_id=user_id,
            product_id=product_id
        )
        if existingRating:
            db.session.delete(existingRating)
            db.session.commit()
            return True, "Product Rating removed"

        return False, "Product rating removed"
