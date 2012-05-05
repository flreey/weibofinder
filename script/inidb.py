# -*- coding:utf-8 -*- 
"""create db if first use"""
from weibofinder import app, db
#from weibofinder.models.base import db
db.init_app(app)
app.test_request_context().push()
db.create_all()

