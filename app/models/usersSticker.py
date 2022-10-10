from flask import current_app
import datetime
import shortuuid
db = current_app.config['db']
BaseModel = current_app.config['BaseModel']


class UsersSticker(BaseModel):
    __tablename__ = 'tb_usersSticker'
    id = db.Column(db.String(28), primary_key=True,
                   )
    user = db.Column(db.String(20))
    deletedAt = db.Column(db.DateTime(timezone=True))
    updatedAt = db.Column(db.DateTime(timezone=True))
    createdAt = db.Column(db.DateTime(timezone=True),
                          default=datetime.datetime.now())
    _default_fields = [
        "id",
        "user",
        "deletedAt",
        "updatedAt",
        "createdAt",
    ]

    def __init__(self,   user,):
        self.user = user

    def delete(self):
        self.deletedAt = datetime.datetime.now()
        db.session.commit()

    def update(self):
        self.updatedAt = datetime.datetime.now()
        db.session.commit()

    def save(self):
        self.id = shortuuid.ShortUUID().random(length=20)
        db.session.add(self)
        db.session.commit()
        db.session.flush()
        return self.id
