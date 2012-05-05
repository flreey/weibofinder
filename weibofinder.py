# -*- coding:utf-8 -*- 

from flask import Flask, jsonify, json
from flask import Flask, redirect, request, render_template, session, jsonify
from models.msg import Msg
from models.base import db
from lib.service import Service, ServiceType, get_oauth
from region_dis import get_offset_cube


app = Flask(__name__)
app.config.from_object('config.local')
db.init_app(app)

@app.route('/search/<float:lng>/<float:lat>', methods=['GET'])
def index(lat, lng):
    session['since_id'] = 0
    return render_template('index.html', lat=lat, lng=lng)

@app.route('/asyn/<float:lng>/<float:lat>', methods=['GET'])
def asyn(lat, lng):
    r = get_offset_cube(lat, lng, 1000)
    msgs = Msg.get_all_points(r)
    msgs = [{'id': m.id, 'lat': m.lat, 'lng': m.lng, 'photo': m.photo, 'weibo_id':
        m.weibo_id} for m in msgs]
    print len(msgs)
    return jsonify(success=True, msgs=msgs)

@app.route('/update', methods=['GET'])
def update():
    #session['userid'], session['token'], session['expires_in']
    oauth = get_oauth()
    if not oauth:
        return redirect('/oauth')
    try:
        mentions = oauth.statuses__mentions(since_id=session.get('since_id', 0))
        #mentions = oauth.statuses__mentions(since_id=0)

        statuses = mentions.statuses

        msg = ''
        for s in statuses:
                coor = s['geo']['coordinates']
                if coor:
                    coordinate = '%s,%s' % (coor[1], coor[0])
                    addr = oauth.get.location__geo__geo_to_address(coordinate=coordinate)['geos'][0]
                    avatar = s['user']['profile_image_url']
                    session['since_id'] = s.id

                    msg = Msg(coor[0], coor[1], s['bmiddle_pic'],
                            s['text'], s['user']['id'], avatar,
                            s['id'], addr['city_name'], addr['province_name'],
                            addr['address'], s['created_at'])
                    msg.save()
    except Exception as e:
            print e

    return jsonify(success=True, msg='x')

@app.route('/oauth', methods=['GET', 'POST'])
def oauth():
    code = request.args.get('code')
    s = Service(ServiceType.WEIBO)

    if not code:
        auth_url = s.get_authorize_url()
        return redirect(auth_url)

    auth, r = s.init_token(code)
    uid = auth.account__get_uid().uid
    session['userid'] = uid
    session['token'] = r.access_token
    session['expires_in'] = r.expires_in

    #oauth = OAuth.get_by_ser_uid(uid)

    #if oauth:
        #session['userid'] = oauth.id
    #else:
        #oauth = OAuth()
        #oauth.ser_uid = uid
        #oauth.service = 'weibo'
        #oauth.save()
        #session['userid'] = oauth.id
    return redirect('/')

def main():
    app.debug = True
    host = '0.0.0.0'
    port = 5000
    app.run(host, port)

if __name__ == '__main__':
    main()
