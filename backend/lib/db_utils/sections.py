from models.section import Section
from extensions import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
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
            return None, "Invalid Name found"
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
            try:
                db.session.delete(section)
                db.session.commit()
                return True, "Section Deleted"
            except IntegrityError as e:
                return None, "Section Contains Products"
            except SQLAlchemyError as e:
                return None, str(e.__dict__['orig'])

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
        print("section Id", section_id, flush=True)
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
        except IntegrityError as e:
            return None, "Section Request with same name already exists"
        except SQLAlchemyError as e:
            return None, str(e.__dict__['orig'])

    def updateSectionRequest(self, section_req_id, name, unit):
        # validation for name
        if (Validators.name(name=name)):
            return None, "invalid name"

        # validation for unit
        if (Validators.checkStringForNull(unit)):
            return None, "unit can't be empty"

        # now checking if a section already exists with same name
        # existingSection = self.checkIfSectionExists(name=name)
        # if a section with same name exists already then we will check if reg_section_id matches with it or not
        # if existingSection and reg_section_id and existingSection.id != reg_section_id:
        #     return False, "A section already exists with new name provided"
        try:
            sectionRequest, message = self.getSectionRequestById(
                section_id=section_req_id)
            if sectionRequest:
                sectionRequest.name = name
                sectionRequest.unit = unit
                db.session.commit()
                return sectionRequest, "Section Request Updated"
            else:
                return None, message
        except SQLAlchemyError as e:
            return None, str(e.__dict__['orig'])

    def getSectionRequestById(self, section_id):
        if Validators.checkForInt(section_id):
            section = SectionRequest.query.get(section_id)
            return section, "Section Found"

        else:
            return None, "invalid section_id"

    def deleteSectionRequestById(self, section_id):
        # fetch section from section requests table
        section, message = self.getSectionRequestById(section_id=section_id)
        # if section is found
        if section:
            db.session.delete(section)
            db.session.commit()
            return True, "Section Request deleted"
        else:
            return False, "Section not found"

    def deleteSectionRequest(self, sectionRequest):
        try:
            db.session.delete(SectionRequest)
            db.session.commit()
            return True, "Section Request deleted"
        except SQLAlchemyError as e:
            print(e)
            return False, "error occured"

    def getEmptySections(self):
        emptySections = Section.query.filter(~Section.products.any()).all()
        return emptySections

    def getNonEmptySections(self):
        nonEmptySections = Section.query.filter(Section.products.any()).all()
        return nonEmptySections
