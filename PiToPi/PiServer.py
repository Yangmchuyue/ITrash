import socket

host = ''
port = 6009  # arbituary port #


def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind complete.")
    return s


def setupConnection():
    s.listen(2)  # Allows one connection at a time.
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn


def get(b, data):
    dataDict = {b: str(data[1])}
    return dataDict[b]  # insert raspi to arduino communication


def dataTransfer(conn):
    while True:     # A big loop that sends/receives data until told not to.
        data = conn.recv(1024)  # receive the data
        data = data.decode('utf-8')
        # Split the data such that you separate the command from the rest of the data.
        dataMessage = data.split(' ', 1)
        command = dataMessage[0]
        if command == "x":
            print(get("x", dataMessage))
            break
        elif command == 'z':
            print(get("z", dataMessage))
            break
        elif command == 'KILL':
            print("Server is shutting down.")
            s.close()
            break
    conn.close()


s = setupServer()
while True:
    try:
        conn = setupConnection()
        dataTransfer(conn)
    except:
        print("Interrupt")
        break
