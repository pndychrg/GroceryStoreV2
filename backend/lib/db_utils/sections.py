from models.section import Section
from extensions import db
from sqlalchemy.exc import SQLAlchemyError
from methods.validators import Validators


class SectionDB:

    def checkIfSectionExists(self, name):
        section = Section.query.filter_by(name=name)
        if section:
            return section
        else:
            return False

    def addSection(self, name, unit):

        if (Validators.checkStringForNull(name)):
            return None, "Name can't be empty"
        if (Validators.checkStringForNull(unit)):
            return None, "Unit can't be empty"

        #  check if section exists with same name
        if (self.checkIfSectionExists(name) != False):
            return None, "Section with same name already exists"

        new_section = Section(name=name, unit=unit)
        db.session.add(new_section)
        db.session.commit()

        return new_section, "Section Added"

    def getSectionById(self, section_id):
        section = Section.query.get(section_id)
        return section

    def deleteSection(self, section_id):
        section = self.getSectionById(section_id=section_id)
        # TODO check if section doesn't contain products
        # if section and len(section.products) == 0:
        if section:
            db.session.delete(section)
            db.session.commit()
            return True, "Section Deleted"
        # elif section and len(section.products) > 0:
        #     return False
        else:
            return None, "Section not found "

    def updateSection(self, section_id, name, unit):
        # checking if section already exits with name
        existingSection = self.checkIfSectionExists(name=name)
        # now checking if the existing section_id is same as current section id
        # because if section id is same, then essentially same section name is being supplied
        if (existingSection.id != section_id):
            return False, "A Section already exists with new name provided"
        section = self.getSectionById(section_id=section_id)
        if section:
            section.name = name
            section.unit = unit
            db.session.commit()
            return section, "Section Updated"
        else:
            return False, "Section not found with given section_id"
