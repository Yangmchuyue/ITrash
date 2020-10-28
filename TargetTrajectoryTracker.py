import array as arr

def predictCoord(point0,point1,timeDiff):
    xVel = (point1.x-point0.x)/timeDiff
    yVel = (point1.y-point0.y)/timeDiff
    zVel = (point1.z-point0.z)/timeDiff
    g = -9.81
    time = (yVel + (yVel ** 2 + 2 * g * point0.y) ** 0.5)/g
    xCoord = point0.x + xVel * time
    yCoord = 0.0
    zCoord = point0.z + zVel * time
    Coord = arr.array('d',[xCoord,yCoord,zCoord])
    return Coord