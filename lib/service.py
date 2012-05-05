# -*- coding:utf-8 -*- 
from lib.weibo import APIClient
from flask import current_app, session, redirect
#from models.oauth import Oauth

class ServiceType():
    WEIBO = 'weibo'
    TQQ = 'tqq'

class Service(object):
    """docstring for Service"""
    def __init__(self, ser_name='weibo'):
        if ser_name not in ServiceType.__dict__.values():
            raise AttributeError('not provide Service:' + ser_name)

        self.ser_name = ser_name

        if ser_name == 'weibo':
            self.service = ser_name
            self.key = current_app.config['SYNC_SERVICE'][ser_name]['key']
            self.secret = current_app.config['SYNC_SERVICE'][ser_name]['secret']
            self.auth = APIClient(self.key, self.secret,
                    current_app.config['HTTP_DOMAIN'] + '/oauth')
        else:
            raise Exception('still in develop')

    def get_authorize_url(self):
        return self.auth.get_authorize_url()

    def init_token(self, code):
        #only need in login

        r = self.auth.request_access_token(code)
        self.token = r.access_token
        self.expires_in = r.expires_in
        self.auth.set_access_token(r.access_token, r.expires_in)
        return self.auth, r

    def get_oauth_by_id(self, id):
        oauth = Oauth.get(id)

        self.auth.set_access_token(oauth.token, oauth.expires_in)
        return self.auth

def get_oauth():
    try:
        token = session['token']
        expires_in = session['expires_in']
        key = current_app.config['SYNC_SERVICE']['weibo']['key']
        secret = current_app.config['SYNC_SERVICE']['weibo']['secret']

        client = APIClient(key, secret,
                        current_app.config['HTTP_DOMAIN'] + '/oauth')
        client.set_access_token(token, expires_in)
        return client
    except Exception:
        return
