import socket
from _thread import *
import sys

server = socket.gethostbyname(socket.gethostname())
print(server)
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


def read_pos(str):
    str = str.split(",")
    x = str[0]
    y = str[1]
    direction = str[2]
    cycle = str[3]
    animation = str[4]
    health = str[5]
    charecter = str[6]
    dammage = str[7]
    return [int(x), int(y), int(direction), int(cycle), int(animation), int(health), int(charecter), int(dammage)]


# function that gives you the position of a box
def make_pos(pos):
    return str(pos[0]) + "," + str(pos[1]) + "," + str(pos[2]) + "," + str(pos[3]) + "," + str(pos[4])+ "," + str(pos[5]) + "," + str(pos[6])+ "," + str(pos[7])

pos = [[120, 575,0,0,0,210,0,0], [1165, 575,1,0,0,210,0,0]]

def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1 :
                    reply = pos[0]
                elif player == 0:
                    reply = pos[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1