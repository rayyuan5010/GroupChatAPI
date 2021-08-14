from flask import current_app
import datetime
import shortuuid
db = current_app.config['db']
BaseModel = current_app.config['BaseModel']


class FirendList(BaseModel):
    __tablename__ = 'tb_firendList'
    userId = db.Column(db.String(28), primary_key=True,)
    firendId = db.Column(db.String(28), primary_key=True,)
    deletedAt = db.Column(db.DateTime(timezone=True))
    updatedAt = db.Column(db.DateTime(timezone=True))
    createdAt = db.Column(db.DateTime(timezone=True),
                          default=datetime.datetime.now())
    _default_fields = [
        "userId",
        "firendId",
        "deletedAt",
        "updatedAt",
        "createdAt",
    ]

    def __init__(self, userId,
                 firendId):
        self.userId = userId
        self.firendId = firendId

    def delete(self):
        self.deletedAt = datetime.datetime.now()
        db.session.commit()

    def update(self):
        self.updatedAt = datetime.datetime.now()
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()
