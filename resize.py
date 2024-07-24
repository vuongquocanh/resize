import base64
import os

import cv2

LIST_DEVICE = [("0", "0.1", 40, 0), ("1", "1.1", 60, 0), ("2", "6.1", 183, 390), ("3", "6.2", 169, 360),
               ("4", "6.7", 202, 430), ("5", "6.9", 194, 412), ("10", "12.9", 313, 1024),
               ("11", "15.1", 501, 2880), ("12", "10.9", 737, 2360), ("20", "20.1", 501, 2880)]


def generate_avatar_path_v2(img, file_path, file_name):
    for i in LIST_DEVICE:
        resize_img = image_resize(img, i[2])

        if not os.path.exists(file_path + "/Avatars"):
            os.mkdir(file_path + "/Avatars")
        if not os.path.exists(file_path + "/Avatars/" + i[1]):
            os.mkdir(file_path + "/Avatars/" + i[1])

        path_avatar = file_path + "/Avatars/" + i[1] + "/" + file_name
        cv2.imwrite(path_avatar, resize_img)
        if int(i[3]) > 0:
            resize_img_max = image_resize(img, i[3])
            path_avatar = file_path + "/Avatars/" + i[1] + "/0-" + file_name
            cv2.imwrite(path_avatar, resize_img_max)

        # file_location = path_avatar.replace("//", "/")
        # yield file_location


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized