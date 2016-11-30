#!/usr/bin/env python2
# -*- coding: utf-8 -*-

API_KEY = '185839fab47af2675b5e458275215a39'
API_SECRET = 'x7EXrX4c5WgIjAQ9un3SgI4-QYTad7Dx'

from facepp import API,File

class ImageDetector:
    ''' Image Detector class demo'''
    file_path = None
    api = None
    def __init__(self, file_path):
        self.file_path = file_path
        self.api = API(API_KEY, API_SECRET)

    def detect(self):
        file = File(self.file_path)
        middle_result = self.api.detection.detect(img = file)
        result = self.api.wait_async(middle_result["session_id"])
        return len(result['result']['face'])


# if __name__ == '__main__':
#     try:
#         vs = VideoService()
#         device = vs.device_serial()
#         pic = vs.take_picture(device)
#         file_path = '/Users/liran/'
#         timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
#         fullFileName = file_path + timestamp + '.png'
#         print fullFileName
#         vs.save_picture(pic, fullFileName)
#         detector = ImageDetector(fullFileName)
#         print 'Detected ' + str(detector.detect()) + ' face(s)'
#     except VideoException as e:
#         print e.msg