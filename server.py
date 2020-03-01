"""
Crypt-Chat Server module

Author: Kaelan Renaud

Date: February 29th, 2020

Version: 2.0

The Server module handles the intialization and the operation of the server. There are two classes: Server and Client. The Client class is
nested inside the Server class. The Server class only needs a path for the seed to instantiate. Client objects will automatically be
instantiated once a client connects to the server. Server objects will handle all the traffic and broadcasting.
"""


from crypt_module import *
import socket, sys, threading, pickle, json

class Server:

    clients = []

    def __init__(self, path):
        print('[*] Initializing server...')
        self.info, self.pub, self.priv = self.loadSeed(path)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.info['address'], self.info['port']))
        print('[*] Seed loaded, server binding %s:%s' % (self.info['address'], self.info['port']))
        self.start()

    # starts server
    def start(self):
        try:
            # gets the maximum amount of users from the seed and starts listening for connections
            self.server.listen(self.info['max_users'])
            print('[*] Listening for clients...')

            # loops to continuously accept connections and start a thread to handle the client
            while True:
                conn, addr = self.server.accept()
                threading.Thread(target=self.handleClient, args=(conn, addr,)).start()

        except Exception as e:
            print('[!] Error while handling a connection: ' + str(e))

    # handles client connections
    def handleClient(self, conn, addr):

        try:
            # gets username from header connection message
            username = conn.recv(self.info['buffer_size']).decode()
            client = self.Client(self, username, addr, conn)
            self.clients.append(client)
            print('[*] %s has connected: %s:%s' % (client.name, client.address[0], str(client.address[1])))

            # loops to receive messages from the client
            while True:
                try:
                    # receives incoming messages from the client
                    msg = conn.recv(self.info['buffer_size'])
                    if msg:
                        # merges message with the sender's username
                        data = pickle.dumps((msg, username))
                        self.broadcast(data, client)
                    else:
                        conn.close()
                        print('[*] Client disconnected: %s:%s' % (addr[0], addr[1]))

                except Exception as e:
                    print('[!] Error while receiving client messsage: ' + str(e))
                    conn.close()
                    print('[*] Client disconnected: %s:%s' % (addr[0], addr[1]))
                    break

        except Exception as e:
            print('[!] Error while setting up client: ' + str(e))
            conn.close()
            print('[*] Client disconnected: %s:%s' % (addr[0], addr[1]))

    def broadcast(self, msg, client):

        # loops through clients and sends the message if they aren't the sender
        for c in self.clients:

            if c != client:
                try:
                    c.conn.send(msg)
                except Exception as e:
                    print(e)
                    c.conn.close()
                    clients.remove(c)

    def loadSeed(self, path):

        # data loaded from JSON file
        seed = {}

        with open(path, 'r') as file:
            seed = json.load(file)

        # server info to build from
        info = seed['seed']
        keys = seed['key']

        # builds keys from data
        pub = rsa.PublicKey(keys['n'], keys['e'])
        priv = rsa.PrivateKey(keys['n'], keys['e'], keys['d'], keys['p'], keys['q'])

        return info, pub, priv

    class Client:

        def __init__(self, server, name, addr, conn):
            self.server = server
            self.name = name
            self.address = addr
            self.conn = conn
            self.id = self.makeId(server.clients)

        # Makes an id from the list of clients that is being used
        def makeId(self, clientList):

            if len(clientList) == 0:
                return 1

            # list for temporarily storings IDs
            allIds = []

            # loops through client list and grabs the IDs
            for c in clientList:
                allIds.append(c.id)

            # sorts IDs so that the final one is the largest
            allIds = sorted(allIds)

            # grabs the largest ID and increments it by 1 to return a new ID
            newId = allIds[-1] + 1

            return newId

if __name__ == '__main__':
    seedPath = str(input('Enter path for seed: '))
    server = Server(seedPath)
    server.start()
    server.server.close()
