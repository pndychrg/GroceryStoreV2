from extensions import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    availableAmount = db.Column(db.Integer, nullable=False, default=1)
    rate = db.Column(db.Integer)
    manufactureDate = db.Column(db.DateTime)
    expiryDate = db.Column(db.DateTime)
    section_id = db.Column(db.Integer, db.ForeignKey(
        'section.id'), nullable=False)
    # getting section details
    section = db.relationship(
        "Section", backref=db.backref('section'))

    def toJson(self):
        return {
            "id": self.id,
            "name": self.name,
            "rate": self.rate,
            "availableAmount": self.availableAmount,
            "manufactureDate": self.manufactureDate.strftime('%Y-%m-%d') if self.manufactureDate != None else None,
            "expiryDate": self.expiryDate.strftime('%Y-%m-%d') if self.expiryDate != None else None,
            "section": self.section.toJson()
        }
