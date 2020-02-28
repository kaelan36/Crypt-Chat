from PyQt5 import QtCore, QtGui, QtWidgets
from crypt_module import *
import socket, threading, sys, rsa, pickle, json

buffSize = 1024
username = 'User'

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.enterBtn = QtWidgets.QPushButton(self.centralwidget)
        self.enterBtn.setGeometry(QtCore.QRect(210, 460, 75, 23))
        self.enterBtn.setObjectName("enterBtn")
        self.enterBtn.clicked.connect(self.getMsg)
        self.output = QtWidgets.QTextEdit(self.centralwidget)
        self.output.setGeometry(QtCore.QRect(80, 30, 641, 381))
        self.output.setObjectName("output")
        self.output.setReadOnly(True)
        self.msgIn = QtWidgets.QLineEdit(self.centralwidget)
        self.msgIn.setGeometry(QtCore.QRect(290, 460, 241, 20))
        self.msgIn.setObjectName("msgIn")
        MainWindow.setCentralWidget(self.centralwidget)

        # menu bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menubar.setNativeMenuBar(False)
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Crypt Chat"))
        self.enterBtn.setText(_translate("MainWindow", "Send"))

    def changeTitle(self, MainWindow, title):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", title))

    def getMsg(self):

        msg = self.msgIn.text()

        if msg == '!quit!':
            server.close()
            quit()

        else:
            threading.Thread(target=send, args=(self, msg,)).start()

    def getPath(self, MainWindow):
        path = QtWidgets.QFileDialog.getOpenFileName(MainWindow, 'Load', './', "JSON Files (*.json)", '')
        return path[0]

    def getUsername(self, MainWindow):
        name, pressed = QtWidgets.QInputDialog.getText(MainWindow, 'Set username', 'Enter username:', QtWidgets.QLineEdit.Normal, '')
        if pressed and name != '':
            return name

def receive(ui, server):
    while True:
        try:
            # receives data and separates actual message from the user address
            msg = server.recv(buffSize)
            msg = pickle.loads(msg)
            msgString = decryptMsg(msg[0], priv)
            sender = str(msg[1])
            msg = '<%s> %s' % (sender, msgString)
            ui.output.append(msg)
        except OSError as e:
            print(e)
            break

def send(ui, msg, event=None):
    ui.output.append('<Me> '+msg)
    msg = encryptMsg(msg, pub)
    server.send(msg)

# loads server with keys using file
def loadSeed(path):

    # values for building keys
    keyVals = {}

    # info for connecting to server
    serverInfo = {}

    with open(path, 'r') as file:
        data = json.load(file)
        keyVals = data['key']
        serverInfo = data['seed']

    pub = rsa.PublicKey(keyVals['n'], keyVals['e'])
    priv = rsa.PrivateKey(keyVals['n'], keyVals['e'], keyVals['d'], keyVals['p'], keyVals['q'])
    buffer_size = serverInfo['buffer_size']

    return serverInfo, pub, priv, buffer_size

# Connects to server
def connect(address, port, ui, name):

    # gets username
    username = ui.getUsername(MainWindow)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((address, port))
    server.send(bytes(username, 'utf8'))
    ui.changeTitle(MainWindow, name)

    threading.Thread(target=receive, args=(ui, server,)).start()
    return server

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

# loads all the seed data, separates key values to make keys and the server info becomes the 'seed' on its own
seed, pub, priv, buffSize = loadSeed(ui.getPath(MainWindow))

server = connect(seed['address'], seed['port'], ui, seed['name'])

MainWindow.show()
sys.exit(app.exec_())

server.close()
