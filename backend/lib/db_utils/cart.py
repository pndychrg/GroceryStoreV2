from extensions import db
from models.cart import Cart
from models.products import Product
from lib.methods.validators import Validators

validators = Validators()


class CartDB:

    def getCartSum(self, cart):
        cartSum = 0
        for item in cart:
            cartSum += item.totalSum

        return cartSum

    def getCartProducts(self, user_id):
        unboughtcartFor_user = Cart.query.filter_by(user_id=user_id).all()
        cartSum = self.getCartSum(unboughtcartFor_user)
        return unboughtcartFor_user, cartSum

    def addToCart(self, user_id, product_id, numOfProduct):
        # validtions
        if (Validators.checkForInt(numOfProduct) == False):
            return None, "invalid number of items"
        # checking if numOfItems is 0
        if (numOfProduct == 0):
            return None, "invalid number of items"
        # fetching the product from the database
        product = Product.query.get(product_id)
        # Note : user-id is fetched from the jwt token so in theory it should always be present
        if product:
            # check if the numOfProduct is more than the available amount
            if (numOfProduct > product.availableAmount):
                return None, f"Only {product.availableAmount} is available"
            # this is to check if the product exists in cart for the user
            product_inCart = Cart.query.filter_by(
                product_id=product_id, user_id=user_id).first()
            if product_inCart == None:
                totalSum = numOfProduct*product.rate
                new_cart = Cart(
                    user_id=user_id,
                    product_id=product_id,
                    numOfProduct=numOfProduct,
                    totalSum=totalSum
                )
                db.session.add(new_cart)
                db.session.commit()
                return new_cart, f"{product.name} is added to cart"
            else:
                product_inCart.numOfProduct = numOfProduct
                product_inCart.totalSum = numOfProduct*product.rate
                db.session.commit()
                return product_inCart, f"{numOfProduct} {product.name} are added in cart "
        else:
            return None, "Product not found"

    def removeFromCart(self, product_id, user_id):
        print(product_id, user_id, flush=True)
        product_inCart = Cart.query.filter_by(
            user_id=user_id, product_id=product_id).first()
        if product_inCart:
            db.session.delete(product_inCart)
            db.session.commit()

            return True, "Cart Item Deleted"
        else:
            return False, "Cart Item not found"
