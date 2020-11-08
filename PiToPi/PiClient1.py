import socket

# duplicate for each client

host = '192.168.1.73'  # update after setup
port = 6009


def setupSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s


def transmit(message):
    s = setupSocket()
    s.send(str.encode(message))
    # print("closing connection")
    # s.send(str.encode("EXIT"))
    s.close

mesg = "X " + str(12)
transmit(mesg)

