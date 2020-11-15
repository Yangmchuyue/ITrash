import socket
# import sys
import serial as serial
import PiToArduino
from threading import Thread


host = ''
port = 6009  # arbituary port #


def setupServer(): #sets up socket server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind complete.")
    return s


def setupConnection():
    s.listen(2)  # Allows two connection at a time.
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn


def dataTransfer(conn):  # A big loop that sends/receives data until told not to.
    while True:
        data = conn.recv(1024)  # receive the data
        data = data.decode('utf-8')
        dataMessage = data.split(' ', 1)  # Split the data to separate the command from the rest of the data.
        command = dataMessage[0]
        if command == "x":
            keyboardIn = dataMessage[1] + "\n"
            ser.write(keyboardIn.encode('utf-8'))
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


s = setupServer() #set up server
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) #set up arduino comm.
ser.flush()
while True:
    try:
        conn = setupConnection()
        Thread(target=dataTransfer(conn)).start()           #data transfer loop that waits for an input
        Thread(target=PiToArduino.arduinoToPi()).start()    #status info from arduino. Both run simultaneously
    except:
        print("Keyboard Interrupt") # Ctrl C to stop program
        break


