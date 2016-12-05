import datetime
import os
from io import BytesIO

import requests
from video.VideoException import VideoException


class VideoService:
    get_token_params = {'appKey': 'a48e330633804b81bd330b0a375db879', 'appSecret': '24597738ce4b615837d10ca3342ba7db'}
    header = {'content-type': 'application/x-www-form-urlencoded'}
    access_token_params = None

    def __init__(self):
        # get access token during init
        print 'starting to retrieve access token...'
        result = requests.post('https://open.ys7.com/api/lapp/token/get', self.get_token_params, self.header)
        res_json = result.json()
        if res_json['code'] != '200':
            raise VideoException(res_json['code'] + res_json['msg'])
        self.access_token_params = {'accessToken': res_json['data']['accessToken']}

    def take_picture(self):
        print '...Retrieving device list...'
        devices_result = requests.post('https://open.ys7.com/api/lapp/device/list', self.access_token_params,
                                       self.header)
        devices_json = devices_result.json()
        if devices_json['code'] != '200':
            raise VideoException(devices_json['code'] + devices_json['msg'])
        dev = devices_json['data'][0]

        params = self.access_token_params
        params['deviceSerial'] = dev['deviceSerial']
        params['channelNo'] = 1

        print '...Taking picture at ' + dev['deviceName'] + '...'
        pic_result = requests.post('https://open.ys7.com/api/lapp/device/capture', params, headers=self.header)
        pic_json = pic_result.json()
        if pic_json['code'] != '200':
            raise VideoException(pic_json['code'] + pic_json['msg'])

        return pic_json['data']['picUrl']



class Test:
    def test(self):
        return "test"
#
#     def save_to_db(self):
#         name = "test.jpg"
#         uri =  os.path.join(APP_IMG_SAV_PATH, name)
#         count = CountInfo(name, uri, datetime.datetime.now(), 1)
#         db.session.add(count)
#         db.session.flush()
#         db.session.commit()

