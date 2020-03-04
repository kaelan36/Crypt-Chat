# Crypt-Chat
Crypt-Chat is a chatting application that allows users to easily make their own servers to chat privately. The transmissions are encrypted using RSA 512-bit encryption. 
Users are able to generate a server 'seed' using the GUI application, which will be used to run the server from. If you want someone to join your server, you would give them the seed file, as it can be used to connect to a server as well. The seed contains the public and private key values necessary to encrypt and decrypt the messages. The seed also contains the IP and port to connect to.

### Dependencies (Python 3)
* PyQT5
* rsa
* pickle
* json

### Basic tutorial
Firstly, if you wish to make your own server, you have to make a seed. To do this, launch main.py and select the *Create a server* option in the Main Menu.
Then, answer all of the prompts and click the *Generate* button.
Now, in the same directory as the main.py file, you will find a JSON file that has the same name as the server you gave. This is your server 'seed' and key to get on it.
To run the server, run the server.py program and input the path for the seed. If there were no issues, the server will have begun to listen on the address and port given.
To connect to the server, click the *Join room* option in the Main Menu.
Once prompted with a file selection, choose the same file you used to run the server. If the server is running, you will then connect to that chatroom.
