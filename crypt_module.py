"""
Crypt-Chat Encryption module

Author: Kaelan Renaud

Date: February 25th, 2020

Version: 1.0

This module handles the encryption and decryption operations of the project. It uses the RSA module to do this. It uses asymmetrical
cryptography to encrypt and decrypt data. It can also generate keys for the encryption.
"""


import rsa

# generates keys with a given bit size
def genKeys(bit):

    (pubkey, privkey) = rsa.newkeys(bit)

    return pubkey, privkey

# Saves the data for building public and private keys
def saveKeys(path, pub, priv):

    try:
        with open(path, 'w') as file:

            file.write(str(pub['n']) + "\n")
            file.write(str(pub['e']) + "\n")
            file.write(str(priv['d']) + "\n")
            file.write(str(priv['p']) + "\n")
            file.write(str(priv['q']) + "\n")

        print('[*] Keys saved')

    except:
        print('[!] Error: Could not save keys to file')

# Builds keys from data found in file path and returns them
def buildKeys(path):

    try:
        with open(path, 'r') as file:

            data = file.readlines()

            # gets rid of \n from file lines and turns data into ints
            for i in range(len(data)):
                data[i] = int(data[i].strip('\n'))

            pubKey = rsa.PublicKey(data[0], data[1])
            privKey = rsa.PrivateKey(data[0], data[1], data[2], data[3], data[4])

            print('[*] Built keys successfully')

            return pubKey, privKey

    except:
        print('[!] Error: Could not build keys')
        return None


# Encrypts a string with a public key given
def encryptMsg(msg, key):

    msg = msg.encode('utf8')

    encrypted = rsa.encrypt(msg, key)

    return encrypted

# Decrypts an encrypted string using a private key
def decryptMsg(msg, key):

    try:
        msg = rsa.decrypt(msg, key)
        msg = msg.decode('utf8')
    except Exception as e:
        print('[!] Error was raised while decrypting: ' + str(e))

    return msg

def test():

    print("[*] Initializing test\n")

    pub, priv = genKeys(512)

    saveKeys('keys', pub, priv)

    message = "Hello There"

    print(message)

    crypto = encryptMsg(message, pub)
    print('Message encrypted')

    print('Creating a new key from file')
    newPub, newPriv = buildKeys('keys')

    decrypto = decryptMsg(crypto, newPriv)

    print(decrypto)



if __name__ == '__main__':
    pass
