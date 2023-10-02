from extensions import db


class Section(db.Model):

    # init
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    unit = db.Column(db.String(100), nullable=False)
    has_pending_changes = db.Column(db.Integer, default=0)
    section_icon = db.Column(db.LargeBinary)
    # TODO add products ref here later

    def toJson(self):
        return {
            'id': self.id,
            'name': self.name,
            'unit': self.unit,
        }
