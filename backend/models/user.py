from extensions import db


class User(db.Model):

    # initialization
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    profile_data = db.Column(db.LargeBinary)  # Actual Data needed for download
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')

    # roles = db.relationship("Role", secondary='user_roles',
    #                         backref=db.backref('users', lazy='dynamic'))

    def toJson(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "role": self.role,
            "profile_data": self.profile_data
        }
