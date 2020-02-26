"""
Creates a server configuration file to be read when running server.py and also creates a key with it
"""
from crypt_module import *

# list for server info
info = ['','','','','']

# list containing values for building keys
keyVals = ['','','','','']

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

# writes all data to file
def writeData(data, path):

    with open(path, 'w') as file:

        for item in data:
            item = str(item)
            file.write(item+'\n')


if __name__ == '__main__':

    info[0], info[1], info[2], info[3], info[4] = getInfo()

    pub, priv = genKeys(info[3])

    keyVals[0] = str(pub['n'])
    keyVals[1] = str(pub['e'])
    keyVals[2] = str(priv['d'])
    keyVals[3] = str(priv['p'])
    keyVals[4] = str(priv['q'])

    for item in keyVals:
        info.append(item)

    writeData(info, info[0]+'_seed')

    # key for accessing server
    serverKey = [info[1], info[2]]
    for item in keyVals:
        serverKey.append(item)
    writeData(serverKey, info[0]+'_key')
