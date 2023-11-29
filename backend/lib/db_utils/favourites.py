from models.favourites import Favourites
from extensions import db
from lib.methods.validators import Validators
from lib.db_utils.products import ProductDB

validators = Validators()
productDB = ProductDB()


class FavouritesMethods:

    def addToFavourites(self, user_id, product_id):

        # checking for null values
        if Validators.checkForInt(user_id) == False:
            return None, "invalid user_id"

        if Validators.checkForInt(product_id) == False:
            return None, "invalid product_id"
        # checking if product with said product_id exists or not
        if productDB.getProductById(product_id=product_id)[0] == None:
            return None, "invalid product_id"

        # searching in db for existing favItem
        existingFavItem, msg = self.getFavouriteProduct(
            user_id=user_id, product_id=product_id)

        if existingFavItem:
            return True, "Already in favourites"

        new_fav = Favourites(
            user_id=user_id,
            product_id=product_id
        )
        db.session.add(new_fav)
        db.session.commit()
        return True, "Added to Favourites"

    def getFavouriteProduct(self, user_id, product_id):

        # checking for null values
        if Validators.checkForInt(user_id) == False:
            return None, "invalid user_id"

        if Validators.checkForInt(product_id) == False:
            return None, "invalid product_id"

        favProduct = Favourites.query.filter_by(
            user_id=user_id, product_id=product_id).first()
        if favProduct:
            return favProduct, "Product Found"
        else:
            return None, "Product not found in favourites list"

    def removeFromFavourites(self, user_id, product_id):
        # checking for null values
        if Validators.checkForInt(user_id) == False:
            return None, "invalid user_id"

        if Validators.checkForInt(product_id) == False:
            return None, "invalid product_id"

        # searching for favItem in db
        existingFav, mesg = self.getFavouriteProduct(
            user_id=user_id, product_id=product_id)

        if existingFav:
            db.session.delete(existingFav)
            db.session.commit()
            return True, "Product removed from favourites"

        return False, "Product not found in favourites"

    def getFavouritesForUser(self, user_id):

        # validation
        if Validators.checkForInt(user_id) == False:
            return None, "invalid user_id"

        favsForUser = Favourites.query.filter_by(user_id=user_id).all()
        return favsForUser, "Favourites for User"
