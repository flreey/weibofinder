from base import db, ORM
from sqlalchemy import and_

class Msg(db.Model, ORM):
    __tablename__ = 'msg'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    photo = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    weibo_uid = db.Column(db.Integer)
    avatar = db.Column(db.String(200))
    weibo_id = db.Column(db.Integer)
    city = db.Column(db.String(30))
    province = db.Column(db.String(30))
    addr = db.Column(db.String(100))
    create_time = db.Column(db.DateTime)

    def __init__(self, lng=None, lat=None, photo=None, content=None,
            weibo_uid=None, avatar=None, weibo_id=None, city=None,   province=None, addr=None, datetime=None):
        self.lng = lng
        self.lat = lat
        self.photo = photo
        self.content = content
        self.weibo_uid = weibo_uid
        self.avatar = avatar
        self.weibo_id = weibo_id
        self.city = city
        self.province = province
        self.datetime = datetime

    @classmethod
    def get_all_points(cls, cube):
        #print cube
        return cls.query.filter(and_(cls.lat<=cube[0][0],
            cls.lat>=cube[2][0],
            cls.lng>=cube[0][1],
            cls.lng<=cube[1][1])).all()

    @classmethod
    def get_by_weibo_id(cls, wid):
        return Msg.query.filter(cls.weibo_id==wid).first()

    def save(self):
        if not Msg.query.filter(Msg.weibo_id==self.weibo_id).first():
            super(Msg, self).save()
