import time

import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# ret, frame = cap.read()
#
# cv.imwrite("image/i2.png", frame)


img1 = cv.imread(cv.samples.findFile('image/i2.png'), cv.IMREAD_GRAYSCALE)
# img2 = cv.imread(cv.samples.findFile('image/i2.png'), cv.IMREAD_GRAYSCALE)
# if img1 is None or img2 is None:
#     print('Could not open or find the images!')
#     exit(0)
# #-- Step 1: Detect the keypoints using SURF Detector, compute the descriptors
# minHessian = 400
# detector = cv.SIFT_create()
# keypoints1, descriptors1 = detector.detectAndCompute(img1, None)
# keypoints2, descriptors2 = detector.detectAndCompute(img2, None)
#
# #-- Step 2: Matching descriptor vectors with a FLANN based matcher
# # Since SURF is a floating-point descriptor NORM_L2 is used
# matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
# knn_matches = matcher.knnMatch(descriptors1, descriptors2, 2)
#
# #-- Filter matches using the Lowe's ratio test
# ratio_thresh = 0.7
# good_matches = []
# for m,n in knn_matches:
#     if m.distance < ratio_thresh * n.distance:
#         good_matches.append(m)
# print(len(good_matches))
# matchRatio = len(good_matches)/ (len(knn_matches))
# print(matchRatio)
# #-- Draw matches
# img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1]+img2.shape[1], 3), dtype=np.uint8)
# cv.drawMatches(img1, keypoints1, img2, keypoints2, good_matches, img_matches, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
# #-- Show detected matches
# cv.imshow('Good Matches', img_matches)
# cv.waitKey()


"""

test for live sift detection 
"""
while "potato" == "potato" :
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Convert to grayscale
    img2 = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    if img1 is None or img2 is None:
        print('Could not open or find the images!')
        exit(0)
    # -- Step 1: Detect the keypoints using SURF Detector, compute the descriptors
    minHessian = 400
    detector = cv.SIFT_create()
    keypoints1, descriptors1 = detector.detectAndCompute(img1, None)
    keypoints2, descriptors2 = detector.detectAndCompute(img2, None)

    # -- Step 2: Matching descriptor vectors with a FLANN based matcher
    # Since SURF is a floating-point descriptor NORM_L2 is used
    matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
    knn_matches = matcher.knnMatch(descriptors1, descriptors2, 2)

    # -- Filter matches using the Lowe's ratio test
    ratio_thresh = 0.7
    good_matches = []
    for m, n in knn_matches:
        if m.distance < ratio_thresh * n.distance:
            good_matches.append(m)
    print(len(good_matches))
    matchRatio = len(good_matches) / (len(knn_matches))
    print(matchRatio)
    # -- Draw matches
    img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1] + img2.shape[1], 3), dtype=np.uint8)
    cv.drawMatches(img1, keypoints1, img2, keypoints2, good_matches, img_matches,
                   flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    # -- Show detected matches
    cv.imshow('Good Matches', img_matches)

    cv.waitKey(1)
    # time.sleep(1)


"""
"""

# while True:
#     time.sleep(1)
# #
#
# while "potato" != "potato" :
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#
#     # if frame is read correctly ret is True
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break
#
#     # Convert to grayscale
#     gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#
#     # SIFT feature descriptor
#     sift = cv.SIFT_create()
#     kp = sift.detect(gray,None)
#
#     gray = cv.drawKeypoints(gray,kp,gray,flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#
#     # Display the resulting frame
#     cv.imshow('Video', gray)
#
#
#     if cv.waitKey(1) == ord('q'): # Press q to exit
#         break


#
# # When everything done, release the capture
# cap.release()
# cv.destroyAllWindows()