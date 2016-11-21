import requests
from PIL import Image
from io import BytesIO
import time

class VideoService:
    get_token_params = {'appKey': 'a48e330633804b81bd330b0a375db879', 'appSecret': '24597738ce4b615837d10ca3342ba7db'}
    header = {'content-type':'application/x-www-form-urlencoded'}
    access_token_params  = None
    def __init__(self):
        #get access token during init
        print 'starting to retrieve access token...'
        result = requests.post('https://open.ys7.com/api/lapp/token/get', self.get_token_params, self.header)
        res_json = result.json()
        if res_json['code'] != '200':
            raise VideoException(res_json['code'] + res_json['msg'])
        self.access_token_params = {'accessToken': res_json['data']['accessToken']}

    def device_serial(self):
        '''return device info'''
        print 'starting to retrieve device list...'
        devices_result = requests.post('https://open.ys7.com/api/lapp/device/list', self.access_token_params, self.header)
        devices_json = devices_result.json()
        if devices_json['code'] != '200':
            raise VideoException(devices_json['code'] + devices_json['msg'])
        dev = devices_json['data'][0]
        return dev

    def take_picture(self, device):
        '''return picture url'''
        params = self.access_token_params
        params['deviceSerial'] = device['deviceSerial']
        params['channelNo'] = 1

        pic_result = requests.post('https://open.ys7.com/api/lapp/device/capture', params, headers=self.header)
        pic_json = pic_result.json()
        if pic_json['code'] != '200':
            raise VideoException(pic_json['code'] + pic_json['msg'])
        print '...now taking picture at ' + device['deviceName']

        return pic_json['data']['picUrl']

    def save_picture(self, pic_url, path):
        picture_result = requests.get(pic_url)
        img = Image.open(BytesIO(picture_result.content))
        img.save(path)

class VideoException (Exception):
    def __init__ (self, msg):
        self.msg = msg
    def __str__ (self):
        return repr(self.msg)

if __name__=="__main__":
    try:
        vs = VideoService()
        device = vs.device_serial()
        pic = vs.take_picture(device)
        file_path = '/Users/liran/'
        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        fullFileName = file_path + timestamp + '.png'
        print fullFileName
        vs.save_picture(pic, fullFileName)
    except VideoException as e:
        print e.msg
    #print fullFileName











