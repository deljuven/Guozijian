# -*- coding: utf-8 -*-
import cv2
import numpy as np

from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 5

FLANN_INDEX_KDTREE = 0


class SurfMatcher:

    def __init__(self):
        self.orb = cv2.ORB_create()
        self.surf = cv2.xfeatures2d.SURF_create()

    def get_keypoints(self, img):
        # return self.orb.detectAndCompute(img, None)
        return self.surf.detectAndCompute(img, None)

    def get_flann_matcher(self):
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        return cv2.FlannBasedMatcher(index_params, search_params)

    def get_bf_matcher(self):
        return cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    def get_draw_params(self, good, kp1, kp2, img1, img2):
        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()

            h, w = img1.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            if M is not None:
                dst = cv2.perspectiveTransform(pts, M)
                img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
            else:
                dst = None
                img2 = None

        else:
            print "Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT)
            matchesMask = None
            dst = None
            pts = None

        return img2, dict(matchColor=(0, 255, 0),  # draw matches in green color
                          singlePointColor=None,
                          matchesMask=matchesMask,  # draw only inliers
                          flags=2), dst, pts

    def matches(self, origin, target):
        kp1, des1 = self.get_keypoints(origin)
        kp2, des2 = self.get_keypoints(target)
        flann = self.get_flann_matcher()
        matches = flann.knnMatch(des1, des2, k=2)
        # store all the good matches as per Lowe's ratio test.
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)
        if len(good) > MIN_MATCH_COUNT:
            return True, good
        return False, good


if __name__ == '__main__':
    # target = cv2.imread('../imgs/face4.jpg', cv2.IMREAD_GRAYSCALE)  # trainImage
    # source, aim = '../imgs/1.jpg', '../imgs/face5.jpg'
    source, aim = 'D:\\Projects\\web\\monitor\\finder\\static\\data\\img\\pattern.png',\
                  'D:\\Projects\\web\\monitor\\finder\\static\\img\\match.png'
    mx, index = 0, 0
    origin_bgr = cv2.imread(source)  # queryImage
    target_bgr = cv2.imread(aim)  # trainImage
    target = cv2.cvtColor(target_bgr, cv2.COLOR_BGR2GRAY)
    origin = cv2.cvtColor(origin_bgr, cv2.COLOR_BGR2GRAY)
    target_rgb = cv2.cvtColor(target_bgr, cv2.cv2.COLOR_BGR2RGB)
    surf = SurfMatcher()
    kp1, des1 = surf.get_keypoints(origin)
    kp2, des2 = surf.get_keypoints(target)
    print(len(kp1), len(kp2))

    flann = surf.get_flann_matcher()
    matches = flann.knnMatch(des1, des2, k=2)
    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)
        # if len(good) > mx:
        #     index = x
        #     mx = len(good)
    # print(index, mx)
    print(len(good))
    target, draw_params, dst, pts = surf.get_draw_params(good, kp1, kp2, origin, target)
    result = cv2.drawMatches(origin, kp1, target, kp2, good, None, **draw_params)
    if dst is not None:
        _, x_bias, _ = origin_bgr.shape
        point0 = (int(dst.item(0)), int(dst.item(1)-x_bias))
        point1 = (int(dst.item(2)), int(dst.item(3)-x_bias))
        point2 = (int(dst.item(4)), int(dst.item(5)-x_bias))
        point3 = (int(dst.item(6)), int(dst.item(7)-x_bias))

        # point0 = (240, 210)
        # point1 = (309, 207)
        # point3 = (250, 386)
        # point2 = (322, 378)
        print((point0,point1,point2,point3,))
        cv2.line(target_rgb, point0, point1, (0, 255, 0), 3)
        cv2.line(target_rgb, point1, point2, (0, 255, 0), 3)
        cv2.line(target_rgb, point2, point3, (0, 255, 0), 3)
        cv2.line(target_rgb, point3, point0, (0, 255, 0), 3)
        plt.figure(figsize=(19.2, 10.8), dpi=100)
        plt.imshow(target_rgb)
        plt.show()
        plt.close()
    plt.figure(figsize=(19.2, 10.8), dpi=100)
    plt.imshow(result)
    plt.show()
    plt.close()
