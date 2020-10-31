import array as arr

def predictCoord(point0,point1,timeDiff):
    xVel = (point1[0]-point0[0])/timeDiff
    yVel = (point1[1]-point0[1])/timeDiff
    # zVel = (point1[2]-point0[2])/timeDiff
    g = -9.81
    time = (yVel + (yVel*yVel + 2 * g * point0[1]) ** 0.5)/g
    xCoord = point0[0] + xVel * time
    yCoord = 0.0
    # zCoord = point0[2] + zVel * time

    print(xCoord)
    print(yCoord)

    Coord = arr.array('d',[xCoord,yCoord,0.0])
    return Coord