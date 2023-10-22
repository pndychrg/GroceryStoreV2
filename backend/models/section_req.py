from extensions import db


class SectionRequest(db.Model):

    __tablename__ = 'section_request'

    # init
    id = db.Column(db.Integer, primary_key=True)
    reg_section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    request = db.Column(db.String(200))
    name = db.Column(db.String(100), unique=True)
    unit = db.Column(db.String(100))
    # section_icon = db.Column(db.LargeBinary)
    section = db.relationship("Section", backref=db.backref('section_request'))

    def toJson(self):
        return {
            'id': self.id,
            'name': self.name,
            'unit': self.unit,
            'reg_section_id':self.reg_section_id,
            'request':self.request,
            # 'section_icon': self.section_icon
        }
