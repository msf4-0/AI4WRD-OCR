from PIL import Image
"""
Class encapsulating functions to resize image
"""

def resizeFrame(imgcrop, zoom, width, height):
    """
    Function that resizes the crop to the specified zoom level
    :param imgcrop: frame of video
    :param zoom: percentage to zoom
    :param width: width of original image
    :param height: height of the original image
    :return: resized image
    """
    cropped_img = Image.fromarray(imgcrop)

    scale_percent = zoom  # percent of original size
    rewidth = int(width * scale_percent / 100)
    reheight = int(height * scale_percent / 100)

    newsize = (rewidth, reheight)
    return cropped_img.resize(newsize)