import sys
from PyQt5 import QtWidgets, QtCore
from controllers.MainController import MainViewController

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = MainViewController()
    sys.exit(app.exec_())