from models.products import Product
from lib.methods.validators import Validators
from extensions import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime


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

    def addProduct(self, name, availableAmount, rate, manufactureDate, expiryDate, section_id):
        # Validations
        if (Validators.name(name=name)):
            return None, "Name can't be empty"

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
            db.session.delete(product)
            db.session.commit()
            return True, "Product Deleted"
        else:
            return False, "product_id not found"

    def updateProduct(self, product_id, name, availableAmount, rate, manufactureDate, expiryDate, section_id):
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
            return None, "Section Request with same name already exists"
        except SQLAlchemyError as e:
            return None, str(e.__dict__['orig'])