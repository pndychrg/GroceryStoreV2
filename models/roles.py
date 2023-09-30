from extensions import db

class Role(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True,nullable=False)

class UserRoles(db.Model):
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'),primary_key=True)


    # back referencing the tables
    #user = db.relationship("User",backref='user_roles')
    #role = db.relationship("Role",backref="user_roles")