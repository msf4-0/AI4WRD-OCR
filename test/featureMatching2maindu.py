# SIFT descriptor with FLANN matcher
import cv2 as cv
import numpy as np

# Load in reference images
ref1 = cv.imread('image/i2.png', cv.IMREAD_GRAYSCALE)
ref2 = cv.imread('image/i3.png', cv.IMREAD_GRAYSCALE)

# Resize reference images
ref1 = cv.resize(ref1, (640, 480))
ref2 = cv.resize(ref2, (640, 480))

# resized images
ref_images = [ref1, ref2]

cap = cv.VideoCapture(0)  # Video Capture


if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Initiate SIFT feature descriptor
sift = cv.SIFT_create()

# Find keypoints and descriptors of reference images (with SIFT)
kp_ref = [[], []]
des_ref = [[[], []], [[], []]]

for i in range(len(ref_images)):
    kp_ref[i], des_ref[i] = sift.detectAndCompute(ref_images[i], None)

# FLANN parameters for SIFT
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)  # or pass empty dictionary

flann = cv.FlannBasedMatcher(index_params, search_params)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Convert frame to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Find keypoints of the frame
    kp, des = sift.detectAndCompute(gray, None)

    # Find matches
    matches = [[[], []], [[], []]]
    num_matches = [0, 0]
    if len(des) == 0:
        print("empty descriptor")
        break
    # if not any(des_ref):
    #     print("empty descriptor")
    #     break
    for j in range(len(ref_images)):
        matches[j] = flann.knnMatch(des, des_ref[j], k=2)
        num_matches[j] = len(matches[j])

    ratio_thresh = 0.7
    # Filter out good matches?
    goodMatches = [[], []]
    for i in range(2):
        knn_matches = matches[i]
        for m, n in knn_matches:
            if m.distance < ratio_thresh * n.distance:
                goodMatches[i].append(m)

    goodMatchesNum = map(len, goodMatches)
    ratioNum = [first/second for first, second in zip(goodMatchesNum, num_matches)]
    print(ratioNum)

    # Current screen
    gray = cv.drawKeypoints(gray, kp, gray, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv.imshow('Video', gray)

    break

    # Press q to exit
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

print(num_matches)

"""
frame_list = [1, 2, 3]
    frame_list_matchValue = []*3 
    frame_list_matchValue[0] = len(matches_1)/len(kp)

    curent_value = frame_list_matchValue[0]
    index = 0
    for i in range(1, len(frame_list)):
        if frame_list_matchValue[index] > frame_list_matchValue[i]:
            index = i
"""
