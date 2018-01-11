# -*- coding: utf-8 -*-
import os

import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import cv2
import numpy as np
from moviepy.editor import VideoFileClip

# from app import APP_MOV_SAV_PATH
from face.matcher import SurfMatcher

# DEFAULT_OUt = os.path.join(APP_MOV_SAV_PATH, "out.mp4")
DEFAULT_OUt = None


class VideoMatcher:

    def __init__(self, imgPattern):
        self.pattern = cv2.imread(imgPattern)
        self.matcher = SurfMatcher()

    def process_image(self, img):
        # NOTE: The output you return should be a color image (3 channel) for processing video below
        # you should return the final output (image with lines are drawn on lanes)
        target_rgb = img
        # target = cv2.cvtColor(target_bgr, cv2.COLOR_BGR2GRAY)
        # origin = cv2.cvtColor(self.pattern, cv2.COLOR_BGR2GRAY)
        target = cv2.cvtColor(target_rgb, cv2.COLOR_RGB2GRAY)
        origin = cv2.cvtColor(self.pattern, cv2.COLOR_RGB2GRAY)
        # target_rgb = cv2.cvtColor(target_bgr, cv2.cv2.COLOR_BGR2RGB)
        kp1, des1 = self.matcher.get_keypoints(origin)
        kp2, des2 = self.matcher.get_keypoints(target)
        flann = self.matcher.get_flann_matcher()
        matches = flann.knnMatch(des1, des2, k=2)
        # store all the good matches as per Lowe's ratio test.
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)
            # if len(good) > mx:
            #     index = x
            #     mx = len(good)
        target, draw_params, dst, pts = self.matcher.get_draw_params(good, kp1, kp2, origin, target)
        image_pil = Image.fromarray(np.uint8(img))
        draw = ImageDraw.Draw(image_pil)
        if dst is not None:
            _, x_bias, _ = self.pattern.shape
            point0 = (int(dst.item(0)), int(dst.item(1) - x_bias))
            point1 = (int(dst.item(2)), int(dst.item(3) - x_bias))
            point2 = (int(dst.item(4)), int(dst.item(5) - x_bias))
            point3 = (int(dst.item(6)), int(dst.item(7) - x_bias))
            draw.line([point0, point1, point2, point3, point0], width=4, fill='green')
        np.copyto(img, np.array(image_pil))
        return img

    def process_video(self, video, out=DEFAULT_OUt):
        clip = VideoFileClip(video)
        out_clip = clip.fl_image(self.process_image)  # NOTE: this function expects color images!!s
        out_clip.write_videofile(out, audio=False)


if __name__ == "__main__":
    pattern = "D:\\Projects\\web\\monitor\\finder\\static\\data\\img\\pattern.png"
    out = "D:\\Projects\\web\\monitor\\finder\\static\\data\\img\\match.mp4"
    video = "D:\\Projects\\web\\monitor\\finder\\static\\video\\5.mp4"
    matcher = VideoMatcher(pattern)
    matcher.process_video(video, out)
