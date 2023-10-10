from models.section import Section
from extensions import db
from sqlalchemy.exc import SQLAlchemyError
from lib.methods.validators import Validators
from models.section_req import SectionRequest


class SectionDB:

    def checkIfSectionExists(self, name):
        section = Section.query.filter_by(name=name).first()
        if section:
            return section
        else:
            return False

    def addSection(self, name, unit):
        if (Validators.name(name)):
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
        if Validators.checkForInt(section_id):
            section = Section.query.get(section_id)
            return section, "Section Found"
        else:
            return None, "Invalid section_id"

    def deleteSection(self, section_id):
        section, message = self.getSectionById(section_id=section_id)
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
        # print(type(existingSection.id), type(section_id), flush=True)
        # now checking if the existing section_id is same as current section id
        # because if section id is same, then essentially same section name is being supplied
        if existingSection and (existingSection.id != int(section_id)):
            return False, "A Section already exists with new name provided"
        section, message = self.getSectionById(section_id=section_id)
        if section:
            section.name = name
            section.unit = unit
            db.session.commit()
            return section, "Section Updated"
        else:
            return False, "Section not found with given section_id"

    def getAllSections(self):
        sections = Section.query.all()
        return sections

    # these functions are used for manager requesting changes in sections

    def getAllSectionRequests(self):
        sections = SectionRequest.query.all()
        if sections:
            return sections, "section found"
        else:
            return None, "section not found"

    def addSectionRequest(self, name, unit, request, reg_section_id=None):
        if (Validators.name(name=name)):
            return None, "invalid name"

        if (Validators.checkStringForNull(unit)):
            return None, "unit can't be empty"
        # check if section already exists with same name
        # this check will be done in sections table
        # if (self.checkIfSectionRequestExists(name) != False):
        #     return None, "section with same name already exists"
        try:
            new_section = SectionRequest(
                name=name, unit=unit, request=request, reg_section_id=reg_section_id)

            db.session.add(new_section)
            db.session.commit()
            return new_section, "Section Request Added"
        except SQLAlchemyError as e:
            return None, str(e)

    def getSectionRequestById(self, section_id):
        if Validators.checkForInt(section_id):
            section = SectionRequest.query.get(section_id)
            return section, "Section Found"

        else:
            return None, "invalid section_id"
