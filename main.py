from PyQt5 import QtCore, QtGui, QtWidgets
from crypt_module import *
import socket, threading, sys, rsa, pickle, json, os

# Class of the Main Window that will be used for display
class uiMainWindow(object):
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setObjectName('MainWindow')
        self.mainMenu()

    def mainMenu(self):
        MainWindow.resize(300, 200)

        self.centralWidget = QtWidgets.QWidget(self.MainWindow)
        self.centralWidget.setObjectName('centralWidget')

        self.title = QtWidgets.QLabel(self.centralWidget)
        self.title.setGeometry(QtCore.QRect(75, 10, 150, 25))
        self.title.setObjectName('title')
        self.title.setText('Welcome to Crypt-Chat')

        self.joinBtn = QtWidgets.QPushButton(self.centralWidget)
        self.joinBtn.setGeometry(QtCore.QRect(75, 45, 150, 25))
        self.joinBtn.setObjectName('joinBtn')
        self.joinBtn.setText('Join room')
        self.joinBtn.clicked.connect(self.chatRoom)

        self.createBtn = QtWidgets.QPushButton(self.centralWidget)
        self.createBtn.setGeometry(QtCore.QRect(75, 80, 150, 25))
        self.createBtn.setObjectName('createBtn')
        self.createBtn.setText('Create a server')
        #self.createBtn.clicked.connect()

        self.profileBtn = QtWidgets.QPushButton(self.centralWidget)
        self.profileBtn.setGeometry(QtCore.QRect(75, 115, 150, 25))
        self.profileBtn.setObjectName('profileBtn')
        self.profileBtn.setText('View Profile')
        #self.profileBtn.clicked.connect()

        self.exitBtn = QtWidgets.QPushButton(self.centralWidget)
        self.exitBtn.setGeometry(QtCore.QRect(75, 150, 150, 25))
        self.exitBtn.setObjectName('exitBtn')
        self.exitBtn.setText('Exit')
        self.exitBtn.clicked.connect(self.exit)

        self.MainWindow.setCentralWidget(self.centralWidget)

    def chatRoom(self):

        # loads keys and info for chat room
        self.seed, self.pub, self.priv, self.buffSize = loadSeed(self.getPath())
        self.server = connect(self, self.seed['address'], self.seed['port'], self.seed['name'], self.priv)

        self.MainWindow.resize(800, 600)
        if self.centralWidget != None:
            self.centralWidget.destroy()

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName('centralWidget')

        self.enterBtn = QtWidgets.QPushButton(self.centralWidget)
        self.enterBtn.setGeometry(QtCore.QRect(210, 460, 75, 23))
        self.enterBtn.setObjectName("enterBtn")
        self.enterBtn.setText('Send')
        self.enterBtn.clicked.connect(self.sendMsg)

        self.output = QtWidgets.QTextEdit(self.centralWidget)
        self.output.setGeometry(QtCore.QRect(80, 30, 641, 381))
        self.output.setObjectName("output")
        self.output.setReadOnly(True)

        self.msgIn = QtWidgets.QLineEdit(self.centralWidget)
        self.msgIn.setGeometry(QtCore.QRect(290, 460, 241, 20))
        self.msgIn.setObjectName("msgIn")

        MainWindow.setCentralWidget(self.centralWidget)

    def createProfile():
        pass

    def sendMsg(self):
        msg = self.msgIn.text()
        if msg == '!quit!':
            server.close()
            self.mainMenu()
        else:
            threading.Thread(target=send, args=(self, msg,)).start()

    def getPath(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self.MainWindow, 'Load', './', 'JSON Files (*.json)', '')
        return path[0]

    def getUsername(self):
        name, pressed = QtWidgets.QInputDialog.getText(self.MainWindow, 'Set username', 'Enter username:', QtWidgets.QLineEdit.Normal, '')
        if pressed and name != '':
            return name

    def changeTitle(self, title):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate('MainWindow', title))

    def exit(self):
        quit()

# Loads a server seed from a given path; file should be JSON
def loadSeed(path):

    # values for building keys
    vals = {}

    # info for connection
    info = {}

    with open(path, 'r') as file:
        data = json.load(file)
        vals = data['key']
        info = data['seed']

    # builds keys and gets buffer size
    pub = rsa.PublicKey(vals['n'], vals['e'])
    priv = rsa.PrivateKey(vals['n'], vals['e'], vals['d'], vals['p'], vals['q'])
    buffer_size = info['buffer_size']

    return info, pub, priv, buffer_size

def receive(ui, server, priv):
    while True:
        try:
            # receives data and separates message from sender's name
            msg = server.recv(ui.buffSize)
            msg = pickle.loads(msg)
            sender = str(msg[1])
            msg = decryptMsg(msg[0], priv)
            msg = '<%s> %s' % (sender, msg)
            ui.output.append(msg)

        except OSError as e:
            print(e)
            ui.mainMenu()
            break

# sends message to server
def send(ui, msg):
    ui.output.append('<Me> '+msg)
    msg = encryptMsg(msg, ui.pub)
    ui.server.send(msg)

# Connects to a server
def connect(ui, address, port, name, priv):

    # gets the username, default will just be user for now
    username = ui.getUsername()

    # opens socket and connects to server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((address, port))
    server.send(bytes(username, 'utf8'))

    # opens thread to receive messages from server
    threading.Thread(target=receive, args=(ui, server, priv,)).start()
    return server

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = uiMainWindow(MainWindow)

MainWindow.show()
sys.exit(app.exec_())
