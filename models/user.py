from extensions import db

class User(db.Model):

    # initialization
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    profile_data = db.Column(db.LargeBinary) # Actual Data needed for download
    profile_rendered = db.Column(db.Text) # data to render the pic in browser
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(100),nullable=False)

    # role 
    roles = db.relationship("Role",secondary='user_roles',backref=db.backref('users',lazy='dynamic'))

    def toJson(self):
        return {
            "id":self.id,
            "name": self.name,
            "username": self.username,
        }