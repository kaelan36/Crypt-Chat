from PyQt5 import QtCore, QtGui, QtWidgets
from crypt_module import *
import socket, threading, sys, rsa, pickle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverAddr = '127.0.0.1'
port = 4444

server.connect((serverAddr, port))

pub, priv = buildKeys('keys')

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
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
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

    def getMsg(self):

        msg = self.msgIn.text()

        if msg == '!quit!':
            server.close()
            quit()

        else:
            threading.Thread(target=send, args=(self, msg,)).start()

def receive(ui):
    while True:
        try:
            # receives data and separates actual message from the user address
            msg = server.recv(2048)
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

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    threading.Thread(target=receive, args=(ui,)).start()
    MainWindow.show()

    sys.exit(app.exec_())

server.close()
