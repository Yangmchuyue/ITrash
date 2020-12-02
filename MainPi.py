import socket
# import sys
import serial as serial
<<<<<<< HEAD

from threading import Thread
=======
# from threading import Thread
>>>>>>> 49db2fa46cb0dda8ab076c73ff8aca322015446f
import time


host = ''
<<<<<<< HEAD
port = int(input("Port: "))  # arbituary port #


def setupServer(): #sets up socket server
=======
port = 6044  # arbituary port #


def setupServer():  # sets up socket server
>>>>>>> 49db2fa46cb0dda8ab076c73ff8aca322015446f
    print("test")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created.")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind complete.")
    return s


def setupConnection():
<<<<<<< HEAD
    s.listen(2)  # Allows one connection at a time.
=======
    s.listen(1)  # Allows one connection at a time.
>>>>>>> 49db2fa46cb0dda8ab076c73ff8aca322015446f
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn


# A big loop that sends/receives data until told not to.
def dataTransfer(conn):
    while True:
<<<<<<< HEAD
        try:
            data = conn.recv(1024)  # receive the data
            data = data.decode('utf-8')
            dataMessage = data.split(' ', 1)  # Split the data to separate the command from the rest of the data.
            command = dataMessage[0]
            if command == "x":
                keyboardIn = dataMessage[1] + " 20" + "\n"
                ser.write(keyboardIn.encode('utf-8'))
                print(dataMessage[1])
            elif command == 'q':
                print("Server is shutting down.")
                keyboardIn = "q"
                ser.write(keyboardIn.encode('utf-8'))
                s.close()
                # sys.exit()
                break
        except:
            print("Error")
            
    conn.close()

print("test2")
s = setupServer() #set up server
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) #set up arduino comm.
except:
    ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
ser.flush()
time.sleep(3)
conn = setupConnection()
dataTransfer(conn) #data transfer loop that waits for an input
        #dataTransfer(cnn)


=======
        data = conn.recv(1024)  # receive the data
        data = data.decode('utf-8')
        # Split the data to separate the command from the rest of the data.
        dataMessage = data.split(' ', 1)
        command = dataMessage[0]
        if command == "x":
            keyboardIn = dataMessage[1] + " 20" + "\n"
            ser.write(keyboardIn.encode('utf-8'))
            print(dataMessage[1])
            break
        # elif command == 'z':
        #     ser.write(dataMessage[1].encode('utf-8'))
        #     break
        elif command == 'q':
            print("Server is shutting down.")
            s.close()
            # sys.exit()
            break
    conn.close()


print("test2")
s = setupServer()  # set up server
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # set up arduino comm.
ser.flush()
time.sleep(3)
>>>>>>> 49db2fa46cb0dda8ab076c73ff8aca322015446f

while True:
    conn = setupConnection()
    dataTransfer(conn)  # data transfer loop that waits for an input
    # dataTransfer(cnn)
