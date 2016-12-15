import requests
from requests import ConnectionError
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from video.VideoException import VideoException


class VideoService:
    get_token_params = {'appKey': 'a48e330633804b81bd330b0a375db879', 'appSecret': '24597738ce4b615837d10ca3342ba7db'}
    header = {'content-type': 'application/x-www-form-urlencoded'}
    access_token_params = None

    def __init__(self):
        # get access token during init
        print 'starting to retrieve access token...'
        result = self._http_request('https://open.ys7.com/api/lapp/token/get', self.get_token_params, self.header)
        res_json = result.json()
        if res_json['code'] != '200':
            raise VideoException(res_json['code'] + res_json['msg'])
        self.access_token_params = {'accessToken': res_json['data']['accessToken']}

    def take_picture(self, total=3):
        print '...Retrieving device list...'
        devices_result = self._http_request('https://open.ys7.com/api/lapp/device/list', self.access_token_params,
                                            self.header, total)

        devices_json = devices_result.json()
        if devices_json['code'] != '200':
            raise VideoException(devices_json['code'] + devices_json['msg'])
        dev = devices_json['data'][0]

        params = self.access_token_params
        params['deviceSerial'] = dev['deviceSerial']
        params['channelNo'] = 1

        print '...Taking picture at ' + dev['deviceName'] + '...'
        pic_result = self._http_request('https://open.ys7.com/api/lapp/device/capture', params, self.header, total)
        pic_json = pic_result.json()
        if pic_json['code'] != '200':
            raise VideoException(pic_json['code'] + pic_json['msg'])

        return pic_json['data']['picUrl']

    def _http_request(self, url, data, header, total=3):
        session = requests.Session()
        retries = Retry(total=total,
                        backoff_factor=0.3,
                        status_forcelist=[500, 502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))
        try:
            result = session.post(url, data, header)
        except ConnectionError:
            raise VideoException('Exceed max retry times')
        return result


class Test:
    def test(self):
        return "test"
