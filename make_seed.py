"""
Creates a server configuration file to be read when running server.py and also creates a key with it
"""
from crypt_module import *
import json


# writes all data to json file
def writeData(data):
    try:
        with open(data['seed']['name'].lower()+'.json', 'w') as file:
            json.dump(data, file)
            print('[*] Data was written to file')
            return data['seed']['name'].lower()+'.json'
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

def initSeedGen(name, address, port, buffSize, maxUsers):
    # dictionary for json file of data
    data = {}

    # dictionary for server building information
    seedInfo = {}

    # generates keys for encryption
    pub, priv = rsa.newkeys(512)

    seedInfo['name'], seedInfo['address'], seedInfo['port'], seedInfo['buffer_size'], seedInfo['max_users'] = name, address, port, buffSize, maxUsers

    data['seed'] = seedInfo
    data['key'] = getKeyInfo(priv)

    filename = writeData(data)
    return filename
