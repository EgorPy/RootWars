import math


def touched_up(y1, height1, y2, height2):
    #if y1 < (y2 - height2) < (y1 + height1):
    if y1 > y2 + height1:
        return True


def touched_down(y1, height1, y2, height2):
    #if y2 < (y1 + height1) < (y2 + height2):
    if y1 + height1 < y2 + height2:
        return True


def touched_left(x1, width1, x2, width2):
    if x2 < (x1 - width1) < (x2 + width2):
        return True


def touched_right(x1, width1, x2, width2):
    if x2 < (x1 + width1) < (x2 + width2):
        return True


def touched(x1, weight1, x2, weight2, y1, height1, y2, height2):
    if (x1 <= x2 and x2 <= (x1 + weight1)
        and y1 <= y2 and y2 <= (y1 + height1)) \
            or (x1 <= (x2 + weight2) and (x1 + weight1) >= x2
                and y1 <= (y2 + height2) and (y1 + height1) >= y2):
        return True
    else:
        return False


def deg_to_rad(degree):
    return degree * math.pi / 180


def rad_to_deg(radian):
    return radian * 180 / math.pi


def rgb_to_hex(rgb=(0, 0, 0)):
    return "#" + str(hex(r))[2:].rjust(2, "0").upper() + str(hex(g))[2:].rjust(2, "0").upper() + str(hex(b))[2:].rjust(2, "0").upper()


def distance_to_obj(pos1=[0, 0], pos2=[500, 500]):
    x_distance = pos1[0] - pos2[0]
    y_distance = pos1[1] - pos2[1]
    distance = pow(x_distance ** 2 + y_distance ** 2, 0.5)
    return distance


def rotate_to_cord(pos1=[0, 0], pos2=[500, 500]):
    # this function returns an angle to turn to face to given position
    # pos1 = pos of the object that must be turned
    # pos2 = pos of the object to turn to
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
