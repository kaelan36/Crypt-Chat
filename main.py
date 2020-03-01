from PyQt5 import QtCore, QtGui, QtWidgets
from crypt_module import *
from make_seed import initSeedGen
import socket, threading, sys, rsa, pickle, json, os

# Class of the Main Window that will be used for display
class uiMainWindow(QtWidgets.QMainWindow):
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setObjectName('MainWindow')
        self.changeTitle('Crypt-Chat')
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
        self.createBtn.clicked.connect(self.createSeed)

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

        # resets central widget
        self.centralWidget = QtWidgets.QWidget(self.MainWindow)
        self.centralWidget.setObjectName('centralWidget')

        self.enterBtn = QtWidgets.QPushButton(self.centralWidget)
        self.enterBtn.setGeometry(QtCore.QRect(210, 460, 75, 23))
        self.enterBtn.setObjectName("enterBtn")
        self.enterBtn.setText('Send')
        self.enterBtn.clicked.connect(self.sendMsg)
        self.enterBtn.setShortcut("Return")

        self.output = QtWidgets.QTextEdit(self.centralWidget)
        self.output.setGeometry(QtCore.QRect(80, 30, 641, 381))
        self.output.setObjectName("output")
        self.output.setReadOnly(True)

        self.msgIn = QtWidgets.QLineEdit(self.centralWidget)
        self.msgIn.setGeometry(QtCore.QRect(290, 460, 241, 20))
        self.msgIn.setObjectName("msgIn")

        MainWindow.setCentralWidget(self.centralWidget)

    # Changes window to prompt the user for information to generate a seed
    def createSeed(self):

        self.MainWindow.resize(400, 300)

        # resets central widget
        self.centralWidget = QtWidgets.QWidget(self.MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        self.title = QtWidgets.QLabel(self.centralWidget)
        self.title.setObjectName('title')
        self.title.setText('Fill out prompts to generate seed')
        self.title.setGeometry(QtCore.QRect(10, 10, 400, 40))
        self.title.setFont(QtGui.QFont('Verdana', 18, QtGui.QFont.Bold))

        self.nameLbl = QtWidgets.QLabel(self.centralWidget)
        self.nameLbl.setObjectName('nameLbl')
        self.nameLbl.setText('Enter a name for your server:')
        self.nameLbl.setGeometry(QtCore.QRect(10, 70, 174, 25))
        self.nameIn = QtWidgets.QLineEdit(self.centralWidget)
        self.nameIn.setObjectName('nameIn')
        self.nameIn.setGeometry(QtCore.QRect(190, 70, 150, 25))

        self.addrLbl = QtWidgets.QLabel(self.centralWidget)
        self.addrLbl.setObjectName('nameLbl')
        self.addrLbl.setText('Enter IP address to bind to:')
        self.addrLbl.setGeometry(QtCore.QRect(21, 105, 163, 25))
        self.addrIn = QtWidgets.QLineEdit(self.centralWidget)
        self.addrIn.setObjectName('addrIn')
        self.addrIn.setGeometry(QtCore.QRect(190, 105, 150, 25))

        self.portLbl = QtWidgets.QLabel(self.centralWidget)
        self.portLbl.setObjectName('portLbl')
        self.portLbl.setText('Enter port to bind to:')
        self.portLbl.setGeometry(QtCore.QRect(59, 140, 125, 25))
        self.portIn = QtWidgets.QLineEdit(self.centralWidget)
        self.portIn.setObjectName('portIn')
        self.portIn.setGeometry(QtCore.QRect(190, 140, 150, 25))
        self.onlyInt = QtGui.QIntValidator()
        self.portIn.setValidator(self.onlyInt)

        self.buffLbl = QtWidgets.QLabel(self.centralWidget)
        self.buffLbl.setObjectName('buffLbl')
        self.buffLbl.setText('Enter desired buffer size:')
        self.buffLbl.setGeometry(QtCore.QRect(33, 175, 151, 25))
        self.buffIn = QtWidgets.QLineEdit(self.centralWidget)
        self.buffIn.setObjectName('buffIn')
        self.buffIn.setGeometry(QtCore.QRect(190, 175, 150, 25))
        self.buffIn.setValidator(self.onlyInt)

        self.maxLbl = QtWidgets.QLabel(self.centralWidget)
        self.maxLbl.setObjectName('maxLbl')
        self.maxLbl.setText('Enter maximum # of users:')
        self.maxLbl.setGeometry(QtCore.QRect(23, 210, 161, 25))
        self.maxIn = QtWidgets.QLineEdit(self.centralWidget)
        self.maxIn.setObjectName('maxIn')
        self.maxIn.setGeometry(QtCore.QRect(190, 210, 150, 25))
        self.maxIn.setValidator(self.onlyInt)

        self.createBtn = QtWidgets.QPushButton(self.centralWidget)
        self.createBtn.setObjectName('createBtn')
        self.createBtn.setText('Generate')
        self.createBtn.setGeometry(QtCore.QRect(245, 245, 100, 25))
        self.createBtn.clicked.connect(self.spawnSeed)
        self.createBtn.setShortcut("Return")

        self.backBtn = QtWidgets.QPushButton(self.centralWidget)
        self.backBtn.setObjectName('backbtn')
        self.backBtn.setText('Back')
        self.backBtn.setGeometry(QtCore.QRect(10, 245, 75, 25))
        self.backBtn.clicked.connect(self.mainMenu)

        self.MainWindow.setCentralWidget(self.centralWidget)

    # Generates a seed from the inputs given
    def spawnSeed(self):

        filename = initSeedGen(self.nameIn.text(), self.addrIn.text(), int(self.portIn.text()), int(self.buffIn.text()), int(self.maxIn.text()))
        msg = "Seed was saved in this directory as: " + filename

        popup = QtWidgets.QMessageBox()
        popup.setWindowTitle('Seed generated successfully')
        popup.setText(msg)

        popup.exec_()
        self.mainMenu()

    # Allows the user to create a profile for when they join servers
    def createProfile(self):
        pass

    # Grabs message from input box and opens thread to send it to server
    def sendMsg(self):
        msg = self.msgIn.text()
        self.msgIn.setText('')
        if msg == '!quit!':
            server.close()
            self.mainMenu()
        else:
            threading.Thread(target=send, args=(self, msg,)).start()

    # Prompts the user to select a JSON file
    def getPath(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self.MainWindow, 'Load', './', 'JSON Files (*.json)', '')
        return path[0]

    # Prompts the user to input a display name
    def getUsername(self):
        name, pressed = QtWidgets.QInputDialog.getText(self.MainWindow, 'Set username', 'Enter username:', QtWidgets.QLineEdit.Normal, '')
        if pressed and name != '':
            return name

    # for changing the title of the window
    def changeTitle(self, title):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate('MainWindow', title))

    # makes sure to close server connection on the close of the window
    def closeEvent(self, event):
        try:
            self.server.close()
        except:
            pass
        event.accept()

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
if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = uiMainWindow(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
