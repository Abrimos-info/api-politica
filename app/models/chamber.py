from app import db

class ChamberModel(db.Model):
    __tablename__ = 'chamber'
    __table_args__ = {'sqlite_autoincrement': True}

    chamber_id = db.Column(db.String(10), unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    #area_id = db.Column(db.Integer, db.ForeignKey('area.area_id'), nullable=False)
    area_id = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(2))

    def __init__(self, name, chamber_id, area_id, country=""):
        self.name = name
        self.chamber_id = chamber_id
        self.area_id = area_id
        self.country = country

    def json(self):
        obj = {
            'id': self.chamber_id,
            'country': self.country,
            'name': {
                'en_US': self.name
            },
            'area_id': self.area_id
        }
        return obj

    @classmethod
    def find_by_id(cls, _id) -> "ChamberModel":
        return cls.query.filter_by(chamber_id=_id).first()

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
