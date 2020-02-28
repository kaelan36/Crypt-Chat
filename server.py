from crypt_module import *
import socket, sys, threading, pickle, json

# list to contain client connections
clientList = []

# Handles client connections
def handleClient(conn, userAddr):

    while True:

        try:
            msg = conn.recv(seed['buffer_size'])

            if msg:

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

# Loads the public and private key from the server seed
def loadKeys(path):

    # for the values needed to build keys
    keyInfo = []

    with open(path, 'r') as file:

        data = json.load(file)

        for val in data['key']:
            keyInfo.append(data['key'][val])

    pub = rsa.PublicKey(keyInfo[0], keyInfo[1])
    priv = rsa.PrivateKey(keyInfo[0], keyInfo[1], keyInfo[2], keyInfo[3], keyInfo[4])

    return pub, priv

# loads info from server seed and returns dictionary of it
def loadSeed(path):

    # dictionary with seed info
    seed = {}

    with open(path, 'r') as file:
        data = json.load(file)
        seed = data['seed']

    return seed


# grabs the server info from seed
seedPath = str(input('Enter path for server seed: '))
seed = loadSeed(seedPath)
pub, priv = loadKeys(seedPath)

# Creates socket for connecting
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# binds the socket to the address and port
server.bind((seed['address'], seed['port']))

# listens for connections
server.listen(seed['max_users'])
print('[*] Server initialized\n[*] Listening for connections...')

while True:

    conn, clientAddr = server.accept()

    clientList.append(conn)

    print('%s has connected' % (clientAddr[0],))

    threading.Thread(target=handleClient, args=(conn, clientAddr,)).start()

conn.close()
server.close()
