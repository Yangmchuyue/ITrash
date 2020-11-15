import array as arr

def predictCoord(point0,point1,timeDiff):
    xVel = (point1[0]-point0[0])/timeDiff
    yVel = (point1[1]-point0[1])/timeDiff
#
#    print("xVel")
#    print(xVel)
#    print("yVel")
#    print(yVel)
#
    g = -9.81
#    print("(yVel*yVel + 2 * g * point0[1]) ** 0.5")
#    print((yVel*yVel + 2 * g * point0[1]) ** 0.5)
#
    time = (-yVel - (yVel*yVel + 2 * g * point0[1]) ** 0.5)/g
    print("time")
    print(time)
    xCoord = point0[0] + xVel * time
    yCoord = 0.0
#    print("X Coord")
#    print(xCoord)
#    print("Y Coord")
#    print(yCoord)

    Coord = arr.array('d',[xCoord.real,yCoord.real])
    return Coord
