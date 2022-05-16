# create a index.html display in pyqt5 with pyqtwebengine

# import pyqt5
import threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QSplitter, QVBoxLayout, QWidget
import os
import flask_data_manage
import threading
import time
import json
import specs

def closeEvent():
    #print("closeEvent")
    threadFlask.terminate()

threadFlask = threading.Thread(target=flask_data_manage.run).start()

# create a index.html display in pyqt5 with pyqtwebengine
app = QApplication([])
view = QWebEngineView()
# get path of index.html
path = os.path.dirname(os.path.realpath(__file__))
url = QUrl.fromLocalFile(f'{path}/index.html')
view.load(url)

app.aboutToQuit.connect(closeEvent)

# set title of window
view.setWindowTitle('PC Control Center')

# set custom window frame
view.setWindowFlags(Qt.FramelessWindowHint)

# Create a button that will be used to close the window
closeButton = QPushButton(view)
closeButton.setGeometry(QRect(view.width() - 30, 0, 30, 30))
closeButton.setText('X')
closeButton.setStyleSheet("background-color: red; border: none;")
closeButton.clicked.connect(view.close)

minimizeButton = QPushButton(view)
minimizeButton.setGeometry(QRect(view.width() - 61, 0, 30, 30))
minimizeButton.setText('-')
minimizeButton.setStyleSheet("background-color: blue; border: none;")
minimizeButton.clicked.connect(view.showMinimized)

refreshButton = QPushButton(view)
refreshButton.setGeometry(QRect(view.width() - 92, 0, 30, 30))
refreshButton.setText('R')
refreshButton.setStyleSheet("background-color: green; border: none;")
refreshButton.clicked.connect(view.reload)

view.show()
app.exec_()

# kill threadFlask when exit

# TODO: Make it look nice :)

# is there a way to make function on close of window?
# https://stackoverflow.com/questions/56907841/pyqt5-how-to-close-a-window-when-the-x-button-is-clicked
# Thanks bro!

# end of file