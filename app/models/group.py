from flask import current_app
import datetime
import shortuuid
db = current_app.config['db']
BaseModel = current_app.config['BaseModel']


class Group(BaseModel):
    __tablename__ = 'tb_group'
    id = db.Column(db.String(28), primary_key=True,
                   default=shortuuid.ShortUUID().random(length=28))
    name = db.Column(db.String(20))
    owner = db.Column(db.String(28))
    image = db.Column(db.String(255))
    deletedAt = db.Column(db.DateTime(timezone=True))
    updatedAt = db.Column(db.DateTime(timezone=True))
    createdAt = db.Column(db.DateTime(timezone=True),
                          default=datetime.datetime.now())
    _default_fields = [
        "id",
        "name",
        "owner",
        "image",
        "deletedAt",
        "updatedAt",
        "createdAt",
    ]

    def __init__(self,   owner, name="", image=""):
        self.name = name
        self.owner = owner
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
        db.session.flush()
        return self.id
