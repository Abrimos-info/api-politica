from app import db

class ProfessionModel(db.Model):
    __tablename__ = 'profession'
    __table_args__ = {'sqlite_autoincrement': True}

    profession_id = db.Column(db.String(10), unique=True, primary_key=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(2))

    def __init__(self, profession_id, description, country=""):
        self.description = description
        self.profession_id = profession_id
        self.country = country

    def json(self):
        obj = {
            'id': self.profession_id,
            'country': self.country,
            'description': self.description
        }
        return obj

    @classmethod
    def find_by_id(cls, _id) -> "ProfessionModel":
        return cls.query.filter_by(profession_id=_id).first()

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
