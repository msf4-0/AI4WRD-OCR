import cv2
"""
Class that encapsulates the data class CropData and algorithms that match 
video stream and crops
"""

# todo add a way to call the algorithms depending on the algorithm in crop data

class CropData:
    """
    class encapsulating the crops and corresponding data
    """

    def __init__(self, frame, num, crops=None):
        self.algorithms = []
        self.frame = frame
        self.num = num
        if crops is None:
            self.crops = []
        else:
            self.crops = crops

    def __str__(self):
        return f'Crop {self.num}'

    # depreciated
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


# todo can separate features and algo if needed later

class SiftFlannAlgo:
    """
    Match using sift features and the flann algorithm
    Attributes:
        num (int):
        frame_list (CropData):list of saved crops and corresponding data
        algorithm_data_list :list of data corresponding to algorithms

    """

    def __init__(self, frame_list: [CropData], num: int):
        """ 
        :param frame_list: list of cropdata 
        :param id: id of current algorithm

        """
        self.frame_list = frame_list
        self.num: int = num

        # Initializing detectors and flann
        self.sift_detector = cv2.SIFT_create()
        self.flann_matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
        self.initialize_algorithm_data()

    def __str__(self):
        return "SiftFlannAlgo"

    def initialize_algorithm_data(self):
        self.algorithm_data_list = [self.precompute(aframe.frame) for aframe in self.frame_list]

    def precompute(self, frame):
        """
        return sift descriptors for each frame
        :return:
        """
        print(type(frame))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        _, descriptors = self.sift_detector.detectAndCompute(frame, None)
        return descriptors

    def process_video_frame(self, video_frame):
        """

        :param video_frame:
        :return: the crops which data best matches the data of the current video stream, index of the crop
        :rtype:
        """
        video_frame = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
        _, frame_descriptors = self.sift_detector.detectAndCompute(video_frame, None)

        max_match_ratio = 0
        max_match_index = 0
        for i in range(len(self.algorithm_data_list)):
            if (frame_descriptors is None) or (self.algorithm_data_list[i] is None):
                break
            if len(frame_descriptors) != 0 and len(self.algorithm_data_list[i]) != 0:
                matches = self.flann_matcher.knnMatch(frame_descriptors, self.algorithm_data_list[i], 2)

                threshold = 0.7
                good_matches = []
                for m, n in matches:
                    if m.distance < threshold * n.distance:
                        good_matches.append(m)
                current_match_ratio = len(good_matches) / (len(matches))

                # code to update the max_match_ratio with the largest match
                if max_match_ratio < current_match_ratio:
                    max_match_index = i
                    max_match_ratio = current_match_ratio

            else:
                pass

        return self.frame_list[max_match_index].crops, max_match_index