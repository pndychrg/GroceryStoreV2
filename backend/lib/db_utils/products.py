from sqlalchemy import func
from models.products import Product
from lib.methods.validators import Validators
from extensions import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime
from models.favourites import Favourites


class ProductDB:

    def getAllProducts(self):
        products = Product.query.all()
        return products

    def getAllProductsBySectionId(self, section_id):
        products = Product.query.filter_by(section_id=section_id).all()

        if products:
            return [product.toJson() for product in products], 200
        else:
            return [], 200

    def getProductById(self, product_id):
        if Validators.checkForInt(product_id):
            product = Product.query.get(product_id)
            return product, "Product Found"
        else:
            return None, "Invalid product_id"

    def addProduct(self, name, description, availableAmount, rate, manufactureDate, expiryDate, section_id):
        # Validations
        if (Validators.name(name=name)):
            return None, "Invalid Product name"

        if (Validators.checkForInt(availableAmount) == False):
            return None, "invalid available amount"
        if (Validators.checkForInt(rate) == False):
            return None, "invalid rate"

        if (Validators.checkDate(manufactureDate) == False):
            return None, "invalid manufacture date"
        else:
            manufactureDate = datetime.strptime(
                manufactureDate, "%Y-%m-%d").date() if (manufactureDate != None) and (len(manufactureDate) != 0) else None

        if (Validators.checkDate(expiryDate) == False):
            return None, "invalid expiry date"
        else:
            expiryDate = datetime.strptime(
                expiryDate, "%Y-%m-%d").date() if (expiryDate != None) and (len(expiryDate) != 0) else None
        try:
            new_product = Product(
                name=name,
                description=description,
                availableAmount=availableAmount,
                rate=rate,
                manufactureDate=manufactureDate,
                expiryDate=expiryDate,
                section_id=section_id
            )

            db.session.add(new_product)
            db.session.commit()

            return new_product, "Product Added"
        except IntegrityError as e:
            return None, "Product with same name already exists"
        except SQLAlchemyError as e:
            return None, str(e.__dict__['orig'])

    def deleteProductById(self, product_id):
        # fetching the product from the database
        product, message = self.getProductById(product_id)

        if product:
            try:
                db.session.delete(product)
                db.session.commit()
                return True, "Product Deleted"
            except IntegrityError as e:
                return None, "Product exists in Bills"
            except SQLAlchemyError as e:
                return None, str(e.__dict__['orig'])

        else:
            return False, "product_id not found"

    def updateProduct(self, product_id, name, availableAmount, rate, manufactureDate, expiryDate, section_id, description):
        # validation for name
        if (Validators.name(name=name)):
            return None, "invalid name"

        if (Validators.checkForInt(availableAmount) == False):
            return None, "invalid available amount"

        if (Validators.checkForInt(rate) == False):
            return None, "invalid rate"

        if (Validators.checkDate(manufactureDate) == False):
            return None, "invalid manufacture date"
        else:
            manufactureDate = datetime.strptime(
                manufactureDate, "%Y-%m-%d").date() if (manufactureDate != None) and (len(manufactureDate) != 0) else None

        if (Validators.checkDate(expiryDate) == False):
            return None, "invalid expiry date"
        else:
            expiryDate = datetime.strptime(
                expiryDate, "%Y-%m-%d").date() if (expiryDate != None) and (len(expiryDate) != 0) else None
        try:
            product, message = self.getProductById(product_id)
            if product:
                product.name = name
                product.description = description
                product.availableAmount = availableAmount
                product.rate = rate
                product.manufactureDate = manufactureDate
                product.expiryDate = expiryDate
                product.section_id = section_id

                db.session.commit()
                return product, "Product Updated"
            else:
                return None, message
        except IntegrityError as e:
            return None, "Product with same name already exists"
        except SQLAlchemyError as e:
            return None, str(e.__dict__['orig'])

    def addProductImage(self, product_id, image):
        # fetching the product from product id
        product, msg = self.getProductById(product_id=product_id)
        if product:
            product.img = image
            db.session.commit()
            return product, "Image Uploaded Successfully"
        else:
            return None, "Product not found"

    def search_products(self, name=None, section_id=None, manufacture_date=None, rate=None):

        query = Product.query
        if name:
            query = query.filter(Product.name.like(f"%{name}%"))
        if section_id:
            query = query.filter(Product.section_id == section_id)
        if rate:
            query = query.filter(Product.rate <= rate)
        if manufacture_date:
            # converting the manufacture_date
            manufacture_date = datetime.strptime(manufacture_date, "%Y-%m-%d")
            query = query.filter(Product.manufactureDate <= manufacture_date)

        products = query.all()
        return products, "Products found"

    def getUnavailableProduct(self):
        unavailableProducts = Product.query.filter(
            Product.availableAmount == 0).all()

        return unavailableProducts

    def getMostRecentProducts(self, limit):
        recentProducts = Product.query.order_by(
            Product.id.desc()).limit(limit=limit)
        return recentProducts

    def getMostFavouredProduct(self):
        mostFavProudct = db.session.query(
            Product,
            func.count(Favourites.id).label('fav_count')
        ).join(Favourites).group_by(Product.id).order_by(
            func.count(Favourites.id).desc()
        ).first()
        # print(mostFavProudct[0].toJson())
        return mostFavProudct[0]

    def getHighestRatedProduct(self):
        products = Product.query.all()
        # sort the products according to avg_rating
        sorted_products = sorted(
            products, key=lambda x: x.avg_rating or 0, reverse=True)
        # print(sorted_products[0].toJson())
        return sorted_products[0]
