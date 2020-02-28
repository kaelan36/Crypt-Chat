from crypt_module import *
import socket, sys, threading, pickle, json

# dict to contain client connections
clients = {}

# handles the initial connection of the client 
def handleConnection(conn, userAddr):
    while True:
        try:
            username = conn.recv(seed['buffer_size']).decode()
            newID = makeid()
            print(newID)
            clients[newID] = (conn, userAddr, username)
            handleClient(conn, userAddr, username, newID)
            break
        except Exception as e:
            print('[!] Error while connecting to client: ' + str(e))

# Handles client connections
def handleClient(conn, userAddr, username, id):

    while True:

        try:
            msg = conn.recv(seed['buffer_size'])
            print(msg)
            if msg:

                # couples data with address
                data = (msg, username)
                msg = pickle.dumps(data)

                # sends message to other connections
                broadcast(msg, conn, userAddr)

            else:
                if id in clients:
                    clients.remove(clients[id])

        except OSError as e:
            print(e)
            break

# makes ids for clients
def makeid():
    ids = []
    for c in clients:
        ids.append(c)
    if len(clients) == 0:
        return 1
    else:
        return max(i for i in ids)+1

# broadcasts message to all users that are connected
def broadcast(msg, conn, userAddr):

    for client in clients:

        if clients[client][0] != conn:
            print('[!] Not client')
            try:
                clients[client][0].send(msg)
            except OSError as e:
                print(e)
                client.close()
                if id == client:
                    clients.remove(client)

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

    threading.Thread(target=handleConnection, args=(conn, clientAddr,)).start()

conn.close()
server.close()
