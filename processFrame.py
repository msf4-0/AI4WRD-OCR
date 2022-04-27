import cv2 as cv


class CropData:
    """ class encapsulating the crops and corresponding data
    Attributes:
    """

    def __init__(self, crops):
        self.algorithms = []
        self.crops = crops

    def add_algorithm(self, algo, frame):
        """
        Algorithms are ordered based on the order that they are inserted, thus they should be
        sorted based on the self.num attribute
        :param frame: 
        :param algo: 
        :return:
        """
        algodata = algo.precompute(frame)
        self.algorithms.append((str(algo), algodata))

        # test for correct ordering, if it fails, ensure that the list of algorithms are correctly sorted before 
        # insertion 
        assert len(self.algorithms) - 1 == algo.num
        assert self.algorithms[-1][0] == str(algo)


class SiftFlannAlgo:
    """
    match using
    Attributes:
        num (int):
        framelist (CropData):list of saved crops and corresponding data
        algorithm_data_list :list of data corresponding to algorithms

    """

    def __init__(self, framelist: [CropData], index: int):
        """
        :param framelist:
        """
        self.num: int = 0
        self.framelist = framelist
        self.algorithmdatalist = [] * len(self.framelist)
        for aframe in framelist:
            self.algorithm_data_list = aframe.algorithms[index][1]

        self.sift_detector = cv.SIFT_create()
        self.flann_matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)

    def __str__(self):
        return "SiftFlannAlgo"

    def precompute(self, frame):
        """
        return sift descriptors for each frame
        :return:
        """
        _, descriptors = self.sift_detector.detectAndCompute(frame, None)
        return descriptors

    def process_video_frame(self, video_frame):
        """

        :param video_frame:
        :return: the view corresponding to said algorithm
        :rtype:
        """

        _, framedescriptors = self.sift_detector.detectAndCompute(video_frame, None)

        maxmatchratio = 0
        maxmatchindex = 0
        for i in range(len(self.algorithm_data_list)):
            matches = self.flann_matcher(framedescriptors, self.algorithmdatalist[i], 2)

            threshold = 0.7
            goodmatches = []
            for m, n in matches:
                if m.distance < threshold * n.distance:
                    goodmatches.append(m)
            currentmatchratio = len(goodmatches) / (len(matches))

            # code to update the maxmatchratio with the largest match
            if maxmatchratio < currentmatchratio:
                maxmatchindex = i

        return self.framelist[maxmatchindex].crops


def GetCropViews():
    """
    leftco = st.session_state.cropArr[counter]["left"]
    widthco = st.session_state.cropArr[counter]["width"]
    topco = st.session_state.cropArr[counter]["top"]
    heightco = st.session_state.cropArr[counter]["height"]

    # st.write(leftco)
    # st.write(widthco)
    # st.wprorite(topco)
    # st.write(heightco)

    cap_arr = np.array(st.session_state.cap)

    imgcrop = cap_arr[topco:topco + heightco, leftco:leftco + widthco]
    cropped_img = Image.fromarray(imgcrop)
    """
    pass


'''
v 2 
text localization 
then ocr
z
'''
