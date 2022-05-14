# create a index.html display in pyqt5 with pyqtwebengine

# import pyqt5
import threading

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication
import os
import flask_data_manage
import threading
import time
import json
import specs

def closeEvent():
    #print("closeEvent")
    threadFlask.terminate()

#onlyserver = "onlyserv" in sys.argv
onlyserver = False

threadFlask = threading.Thread(target=flask_data_manage.run).start()

if not(onlyserver):
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

    view.show()
    app.exec_()

    # kill threadFlask when exit

    # TODO: Make it look nice :)

    # is there a way to make function on close of window?
    # https://stackoverflow.com/questions/56907841/pyqt5-how-to-close-a-window-when-the-x-button-is-clicked
    # Thanks bro!

    # end of file