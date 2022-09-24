from flask import current_app
import datetime
import shortuuid
db = current_app.config['db']
BaseModel = current_app.config['BaseModel']


class Message(BaseModel):
    __tablename__ = 'tb_message'
    messageId = db.Column(db.String(50), primary_key=True,)
    receiverId = db.Column(db.String(100),)
    reciveType = db.Column(db.Integer)
    senderId = db.Column(db.String(50))
    messageTime = db.Column(db.DateTime(timezone=True),
                            default=datetime.datetime.now())
    messageType = db.Column(db.Integer)
    messageContent = db.Column(db.String(50))
    messageTabId = db.Column(db.String(50))

    deletedAt = db.Column(db.DateTime(timezone=True))
    updatedAt = db.Column(db.DateTime(timezone=True))
    createdAt = db.Column(db.DateTime(timezone=True),
                          default=datetime.datetime.now())
    _default_fields = [
        "messageId",
        "receiverId",
        "reciveType",
        "senderId",
        "messageTime",
        "messageType",
        "messageContent",
        "messageTabId",
        "deletedAt",
        "updatedAt",
        "createdAt",
    ]

    def __init__(self,
                 messageId,
                 receiverId,
                 senderId,
                 reciveType=0,
                 messageType=0,
                 messageContent="",
                 messageTabId="0"):
        self.messageId = messageId
        self.receiverId = receiverId
        self.reciveType = reciveType
        self.senderId = senderId
        self.messageType = messageType
        self.messageContent = messageContent
        self.messageTabId = messageTabId

    def delete(self):
        self.deletedAt = datetime.datetime.now()
        db.session.commit()

    def update(self):
        self.updatedAt = datetime.datetime.now()
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()
