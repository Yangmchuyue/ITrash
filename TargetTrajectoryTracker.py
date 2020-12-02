import array as arr


def predictCoord(point0, point1, timeDiff):
    xVel = (point1[0]-point0[0])/timeDiff
    yVel = (point1[1]-point0[1])/timeDiff

    a = -9.81

    time1 = (-yVel - (yVel*yVel - 2 * a * point1[1]) ** 0.5)/a
    time2 = (-yVel + (yVel*yVel - 2 * a * point1[1]) ** 0.5)/a

    time = time1.real

    if time2.real >= 0:
        time = time2.real

    xCoord = point1[0] + xVel * time * 0.7
    yCoord = 0.0

    Coord = arr.array('d', [xCoord.real, yCoord.real])
    return Coord
