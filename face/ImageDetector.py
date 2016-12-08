#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time
from io import BytesIO

import requests
from PIL import Image, ImageDraw

from facepp import API, File
from guozijian import APP_IMG_SAV_PATH

API_KEY = '185839fab47af2675b5e458275215a39'
API_SECRET = 'x7EXrX4c5WgIjAQ9un3SgI4-QYTad7Dx'


class ImageDetector:
    ''' Image Detector class demo'''
    file_path = None
    api = None

    def __init__(self, img_url):
        picture_result = requests.get(img_url)
        img = Image.open(BytesIO(picture_result.content))
        timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))
        path = APP_IMG_SAV_PATH + '/' + timestamp + '.png'
        img.save(path)
        self.file_path = path
        self.api = API(API_KEY, API_SECRET)

    def detect(self, width=5):
        file = File(self.file_path)
        middle_result = self.api.detection.detect(img=file)
        result = self.api.wait_async(middle_result["session_id"])
        img_height = result['result']['img_height']
        img_width = result['result']['img_width']
        faces = result['result']['face']
        face_counts = len(faces)
        print 'Detected ' + str(face_counts) + ' face(s)'
        print 'Now drawing faces on picture...'
        image = Image.open(self.file_path)
        draw = ImageDraw.Draw(image)
        for face in faces:
            center_x = face['position']['center']['x']
            center_y = face['position']['center']['y']
            height = face['position']['height']
            width = face['position']['width']
            x0 = (center_x - 0.5 * width) * img_width * 0.01
            y0 = (center_y - 0.5 * height) * img_height * 0.01
            x1 = (center_x + 0.5 * width) * img_width * 0.01
            y1 = (center_y + 0.5 * height) * img_height * 0.01
            # # down
            # draw.line([x0, y0, x1, y0], fill='red', width=width)
            # # up
            # draw.line([x0, y1, x1, y1], fill='red', width=width)
            # # left
            # draw.line([x0, y0, x0, y1], fill='red', width=width)
            # # right
            # draw.line([x1, y0, x1, y1], fill='red', width=width)
            draw.rectangle([x0, y0, x1, y1], outline='red')
        del draw
        image.save(self.file_path)

        # return: face counts
        return face_counts

# if __name__ == '__main__':
#     try:
#         vs = VideoService()
#         url = vs.take_picture()
#         detector = ImageDetector(url)
#         faces = detector.detect()
#         detector.save_to_db(faces)
#     except VideoException as e:
#         print e.msg
