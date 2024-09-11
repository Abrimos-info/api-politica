from app import db
from datetime import date
from app.const import EmptyValues
from app.models.role import RoleModel
from app.models.person import PersonModel

class ContestModel(db.Model):
    __tablename__ = 'contest'
    __table_args__ = {'sqlite_autoincrement': True}

    contest_id = db.Column(db.String(10), unique=True, primary_key=True, nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.area_id'), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    #membership_id_winner = db.Column(db.Integer, db.ForeignKey('membership.membership_id'), nullable=True)
    membership_id_winner = db.Column(db.Integer, nullable=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    election_identifier = db.Column(db.String(3000), nullable=False)
    country = db.Column(db.String(2))

    def __init__(self, area_id, contest_id, title, membership_id_winner, start_date, end_date, election_identifier, country=""):
        self.area_id = area_id
        self.contest_id = contest_id
        self.title = title
        self.membership_id_winner = membership_id_winner
        self.start_date = start_date
        self.end_date = end_date
        self.election_identifier = election_identifier
        self.country = country

    def json(self):
        roles = RoleModel.query.filter_by(contest_id=self.contest_id)
        persons = PersonModel.query.filter_by(contest_id=self.contest_id)

        role_ids = []
        person_ids = []

        for role in roles:
            role_ids.append(role.role_id)

        for person in persons:
            person_ids.append(person.person_id)

        obj = {
            'id': self.contest_id,
            'country': self.country,
            'area_id': self.area_id,
            'title': {
                'en_US': self.title,
            },
            'membership_id_winner': '' if self.membership_id_winner == EmptyValues.EMPTY_INT else self.membership_id_winner,
            'start_date': '' if self.start_date.strftime('%Y-%m-%d') == date.fromisoformat(EmptyValues.EMPTY_DATE).strftime('%Y-%m-%d') else self.start_date.strftime('%Y-%m-%d'),
            'end_date': '' if self.end_date.strftime('%Y-%m-%d') == date.fromisoformat(EmptyValues.EMPTY_DATE).strftime('%Y-%m-%d') else self.end_date.strftime('%Y-%m-%d'),
            'election_identifier': self.election_identifier,
            'role_ids': role_ids,
            'person_ids': person_ids
        }
        return obj

    @classmethod
    def find_by_id(cls, _id) -> "ContestModel":
        return cls.query.filter_by(contest_id=_id).first()

    @classmethod
    def find_all(cls):
        query_all = cls.query.all()
        result = []
        for one_element in query_all:
            result.append(one_element.json())
        return result

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
