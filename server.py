from crypt_module import *
import socket, sys, threading, pickle

addr = '127.0.0.1'
port = 4444
maxUsers = 10


# Creates socket for connecting
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# binds the socket to the address and port
server.bind((addr, port))

# listens for connections
server.listen(maxUsers)

print('[*] Server initialized\n[*] Listening for connections...')

# list to contain client connections
clientList = []

pub, priv = buildKeys('keys')

# Handles client connections
def handleClient(conn, userAddr):

    while True:

        try:
            msg = conn.recv(2048)
            print(msg)

            if msg:

                # prints the message and the user's id
                print('<%s> %s' % (userAddr[0], msg))

                # couples data with address
                data = (msg, userAddr[0])
                msg = pickle.dumps(data)

                # sends message to other connections
                broadcast(msg, conn)

            else:
                if conn in clientList:
                    clientList.remove(conn)

        except OSError as e:
            print(e)
            break

# broadcasts message to all users that are connected
def broadcast(msg, conn):

    for client in clientList:

        if client != conn:

            try:
                client.send(msg)
            except OSError as e:
                print(e)
                client.close()
                if conn in clientList:
                    clientList.remove(conn)

if __name__ == '__main__':

    while True:

        conn, clientAddr = server.accept()

        clientList.append(conn)

        print('%s has connected' % (clientAddr[0],))

        threading.Thread(target=handleClient, args=(conn, clientAddr,)).start()

    conn.close()
    server.close()
