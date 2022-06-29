import sys
from PyQt5 import QtWidgets, QtCore
from controllers.MainController import MainViewController
from utils.config import initConfigFile

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = MainViewController()
    initConfigFile()
    sys.exit(app.exec_())
