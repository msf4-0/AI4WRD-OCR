# SIFT descriptor with FLANN matcher
import cv2 as cv


# Reference images
ref1 = cv.imread('ReferenceImage1.png', cv.IMREAD_GRAYSCALE)
#ref2 = cv.imread('ReferenceImage2.png', cv.IMREAD_GRAYSCALE)

cap = cv.VideoCapture(1) # Video Capture

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Initiate SIFT feature descriptor
sift = cv.SIFT_create()

# Find keypoints and descriptors of reference images (with SIFT)
kp_ref1, des_ref1 = sift.detectAndCompute(ref1,None)
#kp_ref2, des_ref2 = sift.detectAndCompute(ref2,None)

# FLANN parameters for SIFT
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary

flann = cv.FlannBasedMatcher(index_params,search_params)

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
    kp, des = sift.detectAndCompute(gray,None)

    # Find matches (loop for reference images?)
    matches_1 = flann.knnMatch(des,des_ref1,k=2)
    #matches_2 = flann.knnMatch(des,des_ref2,k=2)

    # Need to draw only good matches, so create a mask
    matchesMask1 = [[0,0] for i in range(len(matches_1))]

    # ratio test as per Lowe's paper
    for i,(m,n) in enumerate(matches_1):
        if m.distance < 0.7*n.distance:
            matchesMask1[i]=[1,0]

    draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask1,
                   flags = cv.DrawMatchesFlags_DEFAULT)

    #gray = cv.drawKeypoints(gray,kp,gray,flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    vid_out = cv.drawMatchesKnn(gray,kp,ref1,kp_ref1,matches_1,None,**draw_params)

    # Display the resulting frame
    cv.imshow('Video', vid_out)
    #cv.imshow('Video', gray)

    # Press q to exit
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()