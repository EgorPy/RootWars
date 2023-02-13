""" useful math functions """

import math


def touched_up(y1, height1, y2):  # height2
    """ Checks if one object is touching up of other object """

    # if y1 < (y2 - height2) < (y1 + height1):
    if y1 > y2 + height1:
        return True


def touched_down(y1, height1, y2, height2):
    """ Checks if one object is touching down of other object """

    # if y2 < (y1 + height1) < (y2 + height2):
    if y1 + height1 < y2 + height2:
        return True


def touched_left(x1, width1, x2, width2):
    """ Checks if one object is touching left of other object """

    if x2 < (x1 - width1) < (x2 + width2):
        return True


def touched_right(x1, width1, x2, width2):
    """ Checks if one object is touching right of other object """

    if x2 < (x1 + width1) < (x2 + width2):
        return True


def touched(x1: int, weight1: int, x2: int, weight2: int, y1: int, height1: int, y2: int, height2: int) -> bool:
    """ Checks if one object is touching other object """

    if (x1 <= x2 <= (x1 + weight1) and y1 <= y2 <= (y1 + height1)) or (x1 <= (x2 + weight2) and (x1 + weight1) >= x2 and y1 <= (y2 + height2) and (y1 + height1) >= y2):
        return True
    else:
        return False


def deg_to_rad(degree):
    """ Converts degrees to radians """

    return degree * math.pi / 180


def rad_to_deg(radian):
    """ Converts radians to degrees """

    return radian * 180 / math.pi


def rgb_to_hex(r=0, g=0, b=0):
    """ Converts rgb value to hex value """

    return "#" + str(hex(r))[2:].rjust(2, "0").upper() + str(hex(g))[2:].rjust(2, "0").upper() + str(hex(b))[2:].rjust(2, "0").upper()


def distance_to_obj(pos1=None, pos2=None):
    """ Gets distance between two positions using Pythagorean theorem """

    if pos1 is None:
        pos1 = [0, 0]
    if pos2 is None:
        pos2 = [500, 500]

    x_distance = pos1[0] - pos2[0]
    y_distance = pos1[1] - pos2[1]
    distance = pow(x_distance ** 2 + y_distance ** 2, 0.5)
    return distance


def rotate_to_cord(pos1=None, pos2=None):
    """
    :param pos1: pos of the object that must be turned
    :param pos2: pos of the object to turn to
    :return: angle to turn to face to given position
    """

    if pos1 is None:
        pos1 = [0, 0]
    if pos2 is None:
        pos2 = [500, 500]

    x_distance = pos1[0] - pos2[0]
    y_distance = pos1[1] - pos2[1]
    try:
        angle = math.atan(x_distance / y_distance)
        angle = rad_to_deg(angle)
        if pos1[1] > pos2[1]:
            return angle + 180
        else:
            return angle
    except ZeroDivisionError:
        return None
