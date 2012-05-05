# -*- coding:utf-8 -*- 
from base import db, ORM
from sqlalchemy import and_

class OAuth(db.Model, ORM):
    __tablename__ = 'oauth'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #userid = db.Column(db.Integer, nullable=False)
    ser_uid = db.Column(db.Integer, unique=True, nullable=False)
    service = db.Column(db.String, nullable=False)
    nick_name = db.Column(db.String(20))

    def __init__(self, ser_uid=None, service =None, nick_name=None):
        self.ser_uid = ser_uid
        self.service = service
        self.nick_name = nick_name

    @staticmethod
    def get_by_ser_uid(ser_uid, service='weibo'):
        return OAuth.query.filter(and_(OAuth.ser_uid==ser_uid,
            OAuth.service==service)).first()
