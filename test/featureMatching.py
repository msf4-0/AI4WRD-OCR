import cv2 as cv


cap = cv.VideoCapture(1)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Convert to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # SIFT feature descriptor
    sift = cv.SIFT_create()
    kp = sift.detect(gray,None)

    gray = cv.drawKeypoints(gray,kp,gray,flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Display the resulting frame
    cv.imshow('Video', gray)
    if cv.waitKey(1) == ord('q'): # Press q to exit
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()