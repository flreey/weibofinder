import json
from flask import current_app
from flaskext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()

class ORM(object):
    def save(self):
        db.session.flush()
        db.session.add(self)
        db.session.commit()

    def update(self):
        self._before_update()
        db.session.merge(self)
        db.session.commit()

    def _before_update(self):
        pass

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    def __repr__(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = getattr(self, c.name)
        return '%s' % d
