from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QImage
from utils.opencv import *
import sys

from templates.boundingBoxesMain import MainView

class MainViewController(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = MainView()
        self.ui.setupUi(self)

        # Variables locales
        self.ruta_imagen = ''
        self.ruta_xml = ''

        self.ui.bttn_selectimg.clicked.connect(lambda: self.abrirFotografia())
        self.ui.bttn_boxes.clicked.connect(lambda: self.agregarBoxesImagenListView())
        self.show()

    def abrirFotografia(self):
        filename =  QtWidgets.QFileDialog.getOpenFileName(None, 'Buscar Imagen', '.', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
        
        if filename[0]:
            self.ruta_imagen = filename[0]
            imagen = QImage(self.ruta_imagen)
            pix = QPixmap.fromImage(imagen).scaled(700, 700, QtCore.Qt.KeepAspectRatio)
            self.ui.lbl_titulo.setText(filename[0])
            self.ui.lbl_imagen.setPixmap(pix)
    
    def agregarBoxesImagenListView(self):
        entradas = ["Uno", "Dos", "Tres"]
        self.ui.listView.addItems(entradas)

        imagen_cv = setBoxesToImage(self.ruta_imagen)
        imagen = QImage(imagen_cv.data, imagen_cv.shape[1], imagen_cv.shape[0], QImage.Format_RGB888).rgbSwapped()
        pix = QPixmap.fromImage(imagen).scaled(700, 700, QtCore.Qt.KeepAspectRatio)
        self.ui.lbl_imagen.setPixmap(pix)
