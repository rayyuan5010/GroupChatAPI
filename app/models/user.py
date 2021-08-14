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
    image = db.Column(db.String(100))
    firendCode = db.Column(
        db.String(20), default=shortuuid.ShortUUID().random(length=20))
    deletedAt = db.Column(db.DateTime(timezone=True))
    updatedAt = db.Column(db.DateTime(timezone=True))
    createdAt = db.Column(db.DateTime(timezone=True),
                          default=datetime.datetime.now())
    _default_fields = [
        "id",
        "email",
        "password",
        "name",
        "image",
        "deletedAt",
        "updatedAt",
        "createdAt",
    ]

    def __init__(self, id, email, password, name="新用戶", image=""):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.image = image

    def delete(self):
        self.deletedAt = datetime.datetime.now()
        db.session.commit()

    def update(self):
        self.updatedAt = datetime.datetime.now()
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()
