# -*- coding: utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt

# # Initiate SIFT detector
# sift = cv2.xfeatures2d.SIFT_create()

MIN_MATCH_COUNT = 10

FLANN_INDEX_KDTREE = 0


# Initiate SURF detector
class SurfMatcher:

    def __init__(self):
        self.surf = cv2.xfeatures2d.SURF_create()

    def get_keypoints(self, img):
        return self.surf.detectAndCompute(img, None)

    def get_flann_matcher(self):
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        return cv2.FlannBasedMatcher(index_params, search_params)

    def get_draw_params(self, good, kp1, kp2, img1, img2):
        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()

            h, w = img1.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
        else:
            print "Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT)
            matchesMask = None

        return img2, dict(matchColor=(0, 255, 0),  # draw matches in green color
                          singlePointColor=None,
                          matchesMask=matchesMask,  # draw only inliers
                          flags=2)

    def is_match(self, origin, target):
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
            return True
        return False


if __name__ == '__main__':
    origin = cv2.imread('../imgs/1.jpg', 0)  # queryImage
    target = cv2.imread('../imgs/face3.jpg', 0)  # trainImage
    surf = SurfMatcher()
    kp1, des1 = surf.get_keypoints(origin)
    kp2, des2 = surf.get_keypoints(target)
    flann = surf.get_flann_matcher()
    matches = flann.knnMatch(des1, des2, k=2)
    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)
    target, draw_params = surf.get_draw_params(good, kp1, kp2, origin, target)
    result = cv2.drawMatches(origin, kp1, target, kp2, good, None, **draw_params)

    # plt.imshow(img3, 'gray'), plt.show()
    plt.imshow(result)
    plt.show()
