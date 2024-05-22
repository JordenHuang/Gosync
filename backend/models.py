from .database import db

class User(db.Model):
    __tablename__ = "users"

    def __init__(self, phone, name, nickname, passwd, credit_score):
        self.phone = phone
        self.name = name
        self.nickname = nickname
        self.passwd = passwd
        self.credit_score = credit_score

    phone = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(20))
    # nickname can be empty
    nickname = db.Column(db.String(20))
    passwd = db.Column(db.String(150))
    credit_score = db.Column(db.Integer())

    def __repr__(self):
        return f"phone: {self.phone}, name: {self.name}, nickname: {self.nickname}, passwd: {self.passwd}, credit_score: {self.credit_score}"

    def to_dict(self):
        return {field.name:getattr(self, field.name) for field in self.__table__.c}