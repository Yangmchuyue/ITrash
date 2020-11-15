import array as arr

def predictCoord(point0,point1,timeDiff):
    xVel = (point1[0]-point0[0])/timeDiff
    yVel = (point1[1]-point0[1])/timeDiff
#
    print("point 2 xPos")
    print(point1[0])
    print("point 2 yPos")
    print(point1[1])
#
    a = -9.81
#    print("(yVel*yVel + 2 * g * point0[1]) ** 0.5")
#    print((yVel*yVel + 2 * g * point0[1]) ** 0.5)


    time1 = (-yVel - (yVel*yVel - 2 * a * point1[1]) ** 0.5)/a
    time2 = (-yVel + (yVel*yVel - 2 * a * point1[1]) ** 0.5)/a
    
    time = time1.real

    if time2.real >= 0:
        time = time2.real
    
    

    print("time1")
    print(time1)
    print("time2")
    print(time2)
    
    xCoord = point1[0] + xVel * time
    yCoord = 0.0
#    print("X Coord")
#    print(xCoord)
#    print("Y Coord")
#    print(yCoord)

    Coord = arr.array('d',[xCoord.real,yCoord.real])
    return Coord
