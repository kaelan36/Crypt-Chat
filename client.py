import socket, threading, sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverAddr = '127.0.0.1'
port = 4444

server.connect((serverAddr, port))

def receive():

    while True:
        try:
            msg = server.recv(1024).decode('utf8')
        except:
            break

def getMsg():

    while True:

        msg = input('\nSend: ')

        if msg == '!quit!':
            server.close()
            quit()

        print('Me> ' + msg)

        threading.Thread(target=send, args=(msg,)).start()

def send(msg, event=None):
    server.send(bytes(msg, 'utf8'))

if __name__ == '__main__':

    threading.Thread(target=receive).start()
    getMsg()

server.close()
