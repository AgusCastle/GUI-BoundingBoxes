from logging import root
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QImage, QIcon, QColor
from utils.opencv import *
from utils.xml import xml_annotation
import numpy as np
import sys


from templates.boundingBoxesMain import MainView
from templates.WidgetCourtImage import Ui_Form

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
        self.ui.listView.doubleClicked.connect(self.onCliked)
        self.show()

    def onCliked(self, item):
        index = self.ui.listView.currentRow()
        self.Form = QtWidgets.QDialog()
        ui = Ui_Form()
        h, w, imagen_cv = cutImageBox(self.ruta_imagen, self.imgdata['boxes'][index])
        imagen = QImage(imagen_cv.data.tobytes(), w, h, w * 3, QImage.Format_RGB888).rgbSwapped()
        pix = QPixmap.fromImage(imagen).scaled(450, 450, QtCore.Qt.KeepAspectRatio)
        rad = 0
        
        if self.imgdata['labels'][index] == 'surgical':
            rad = 1

        ui.setupUi(self.Form, pix, rad)
        self.Form.show()

    def abrirFotografia(self):
        filename =  QtWidgets.QFileDialog.getOpenFileName(None, 'Buscar Imagen', '.', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
        
        if filename[0]:
            self.ruta_imagen = filename[0]
            imagen = QImage(self.ruta_imagen)
            pix = QPixmap.fromImage(imagen).scaled(700, 700, QtCore.Qt.KeepAspectRatio)
            self.ui.lbl_titulo.setText(filename[0])
            self.ui.lbl_imagen.setPixmap(pix)
    
    def agregarBoxesImagenListView(self):
        # Obviamente esta harcodeado pero con la funcion que esta se 
        # supone que con esto ya debe de quedar

        filename =  QtWidgets.QFileDialog.getOpenFileName(None, 'Buscar xml', '.', 'Image Files (*.xml)')
        
        if filename[0]:
            self.ruta_xml = filename[0]
        else:
            return

        self.ui.listView.clear()

        self.imgdata = xml_annotation(self.ruta_xml)

        imagen_cv, colors = setBoxesToImage(self.ruta_imagen, self.imgdata)

        for i, c in zip(self.imgdata['labels'], colors):
            label = QtWidgets.QListWidgetItem()
            color = QPixmap(10,10)
            color.fill(QColor(c[2], c[1], c[0]))
            label.setIcon(QIcon(color))
            label.setText(i)
            self.ui.listView.addItem(label)

        self.ui.listView.setStyleSheet(" QListWidget::icon{border:5px;}")
        
        imagen = QImage(imagen_cv.data, imagen_cv.shape[1], imagen_cv.shape[0], QImage.Format_RGB888).rgbSwapped()
        pix = QPixmap.fromImage(imagen).scaled(700, 700, QtCore.Qt.KeepAspectRatio)
        self.ui.lbl_imagen.setPixmap(pix)
