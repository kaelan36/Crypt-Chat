"""
Creates a server configuration file to be read when running server.py and also creates a key with it
"""
from crypt_module import *
import json

# gets info for server connection
def getInfo():

    while True:

        name = str(input("Enter name for the server: "))

        # ip address to connect to
        addr = str(input("Enter IP Address for connection: "))

        try:
            port = int(input("Enter port for connection: "))
            bufSize = int(input("Enter buffer size for data: "))
            maxUsers = int(input("Enter maximum of users for server: "))
            return name, addr, port, bufSize, maxUsers
        except ValueError:
            print('[!] Not a valid port number')


# writes all data to json file
def writeData(data):
    try:
        with open(data['seed']['name'].lower()+'.json', 'w') as file:
            json.dump(data, file)
            print('[*] Data was written to file')
    except Exception as e:
        print('[!] Encountered error while writing to file')
        print(e)


# grabs key info and stores in dictionary to be returned, takes in a private key because they contain all data
def getKeyInfo(key):

    info = {}

    values = ['n', 'e', 'd', 'p', 'q']

    for c in values:
        info[c] = key[c]

    return info

# dictionary for json file of data
data = {}

# dictionary for server building information
seedInfo = {}

# generates keys for encryption
pub, priv = rsa.newkeys(512)

# dictionary for key building information
keyInfo = getKeyInfo(priv)

seedInfo['name'], seedInfo['address'], seedInfo['port'], seedInfo['buffer_size'], seedInfo['max_users'] = getInfo()

data['seed'] = seedInfo
data['key'] = keyInfo

writeData(data)
