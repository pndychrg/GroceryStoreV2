import base64
from extensions import db


class User(db.Model):

    # initialization
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    img = db.Column(db.LargeBinary)  # Actual Data needed for download
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')
    ratings = db.relationship(
        "Rating", backref="rating_byUser", lazy="dynamic"
    )

    def toJson(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "role": self.role,
            # "img": base64.b64encode(self.img).decode('utf-8') if self.img != None else None,
            "email": self.email
        }

    def image(self):
        return {
            # "id": self.id,
            # "name": self.name,
            # "username": self.username,
            # "role": self.role,
            "img": base64.b64encode(self.img).decode('utf-8') if self.img != None else None,
            # "email": self.email
        }
