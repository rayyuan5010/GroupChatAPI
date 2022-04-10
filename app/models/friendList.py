from flask import current_app
import datetime
import shortuuid
db = current_app.config['db']
BaseModel = current_app.config['BaseModel']


class FriendList(BaseModel):
    __tablename__ = 'tb_friendList'
    userId = db.Column(db.String(28), primary_key=True,)
    friendId = db.Column(db.String(28), primary_key=True,)
    accept = db.Column(db.Integer, default=0)
    deletedAt = db.Column(db.DateTime(timezone=True))
    updatedAt = db.Column(db.DateTime(timezone=True))
    createdAt = db.Column(db.DateTime(timezone=True),
                          default=datetime.datetime.now())
    _default_fields = [
        "userId",
        "friendId",
        "accept",
        "deletedAt",
        "updatedAt",
        "createdAt",
    ]

    def __init__(self, userId,
                 friendId, accept=0):
        self.userId = userId
        self.friendId = friendId
        self.accept = accept

    def delete(self):
        self.deletedAt = datetime.datetime.now()
        db.session.commit()

    def update(self):
        self.updatedAt = datetime.datetime.now()
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()
