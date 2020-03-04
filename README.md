# Crypt-Chat
Crypt-Chat is a chatting application that allows users to easily make their own servers to chat privately. The transmissions are encrypted using RSA 512-bit encryption. 
Users are able to generate a server 'seed' using the GUI application, which will be used to run the server from. If you want someone to join your server, you would give them the seed file, as it can be used to connect to a server as well. The seed contains the public and private key values necessary to encrypt and decrypt the messages. The seed also contains the IP and port to connect to.

### Dependencies (Python 3)
* PyQT5
* rsa
* pickle
* json

### Basic tutorial
Firstly, if you wish to make your own server, you have to make a seed. To do this, launch main.py and select the 
