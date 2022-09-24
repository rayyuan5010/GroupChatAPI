from flask import current_app
import datetime
import shortuuid
db = current_app.config['db']
BaseModel = current_app.config['BaseModel']


class User(BaseModel):
    __tablename__ = 'tb_user'
    id = db.Column(db.String(28), primary_key=True,
                   default=shortuuid.ShortUUID().random(length=20))
    email = db.Column(db.String(100),)
    password = db.Column(db.String(50))
    name = db.Column(db.String(20))
    userSM = db.Column(db.String(100))
    image = db.Column(db.String(100))
    friendCode = db.Column(
        db.String(20),  primary_key=True, default=shortuuid.ShortUUID().random(length=10))
    fcmToken = db.Column(db.String(200))
    deletedAt = db.Column(db.DateTime(timezone=True))
    updatedAt = db.Column(db.DateTime(timezone=True))
    createdAt = db.Column(db.DateTime(timezone=True),
                          default=datetime.datetime.now())
    _default_fields = [
        "id",
        "email",
        "password",
        "friendCode",
        "userSM",
        "name",
        "image",
        "fcmToken",
        "deletedAt",
        "updatedAt",
        "createdAt",
    ]

    def __init__(self, id, email, password, name="新用戶", image="", friendCode="", userSM=""):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.image = image
        self.userSM = userSM
        self.friendCode = friendCode

    def delete(self):
        self.deletedAt = datetime.datetime.now()
        db.session.commit()

    def update(self):
        self.updatedAt = datetime.datetime.now()
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()
