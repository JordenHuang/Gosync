from .database import db

'''
Table description:
使用者 -> User
事件 -> event
使用者_事件 (多對多) -> chatroom
聊天室內容 -> Chat_contene
'''

chatroom = db.Table(
    "chatroom",
    db.Column("user_phone", db.String(10), db.ForeignKey("users.phone")),
    db.Column(
        "event_id",
        db.Integer,
        db.ForeignKey("events.event_id"),
    ),
)

class User(db.Model):
    '''
        phone:      使用者手機 (Primary key)
        passwd:     使用者密碼
        name:       使用者姓名
        nickname:   使用者暱稱
        credit_score: 信用分數
    '''
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

class Event(db.Model):
    '''
        event_id:   事件id (Primary key)
        name:       事件名稱
        host:       創辦人
        type:       事件類型
        time:       事件時間
        detail:     事件詳細說明
        meeting_point: 會面點地
        destination: 目標地點
        max_participants: 最大人數
    '''
    __tablename__ = "events"

    def __init__(self, name, host, type, time, detail, meeting_point, destination, max_participants):
        self.name = name
        self.host = host
        self.type = type
        self.time = time
        self.detail = detail
        self.meeting_point = meeting_point
        self.destination = destination
        self.max_participants = max_participants

    event_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    host = db.Column(db.String(20))
    type = db.Column(db.String(20))
    time = db.Column(db.Date)
    detail = db.Column(db.String(100))
    meeting_point = db.Column(db.String(100))
    destination = db.Column(db.String(100))
    max_participants = db.Column(db.Integer)

    def to_dict(self):
        return {field.name:getattr(self, field.name) for field in self.__table__.c}


# class chatroom(db.Model):
#     '''
#     '''
#     __tablename__ = "chatroom"

#     def __init__(self, chatroom_id, user_phone):
#         pass

class Chat_content(db.Model):
    '''
    t_id: 聊天內容id (Primary key)
    time: 發送時間
    event_id: 事件id (Foreign key)
    user_phone: 使用者手機(Foreign key)
    text: 內容
    '''
    __tablename__ = "chat_content"

    def __init__(self, time, event_id, user_phone, text):
        self.time = time
        self.event_id = event_id
        self.user_phone = user_phone
        self.text = text

    t_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"))
    user_phone = db.Column(db.String(10), db.ForeignKey("users.phone"))
    text = db.Column(db.String(500))

    def to_dict(self):
        return {field.name:getattr(self, field.name) for field in self.__table__.c}