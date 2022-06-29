import sys
from PyQt5 import QtWidgets, QtCore
from controllers.MainController import MainViewController
from utils.config import initConfigFile

if __name__ == "__main__":

    initConfigFile()
    app = QtWidgets.QApplication(sys.argv)
    window = MainViewController()
    sys.exit(app.exec_())
