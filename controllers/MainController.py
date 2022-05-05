from logging import root
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QImage, QIcon, QColor
from utils.opencv import *
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
        ui.setupUi(self.Form, pix)
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
        self.ui.listView.clear()
        lista_boxes = list()
        lista_labels = list()

        lista_boxes.append([360, 146, 471, 262])
        lista_labels.append('Box 1')
        lista_boxes.append([38, 66, 109, 145])
        lista_labels.append('Box 2')
        lista_boxes.append([649, 14, 715, 86])
        lista_labels.append('Box 3')
        lista_boxes.append([221, 54, 291, 124])
        lista_labels.append('Box 4')

        self.imgdata = {'name': 'nombreArchivo', 'boxes': lista_boxes, 'labels': lista_labels}

        imagen_cv, colors = setBoxesToImage(self.ruta_imagen, self.imgdata)

        for i, c in zip(self.imgdata['labels'], colors):
            label = QtWidgets.QListWidgetItem()
            color = QPixmap(10,10)
            color.fill(QColor(c[2], c[1], c[0]))
            label.setIcon(QIcon(color))
            label.setText(i)
            self.ui.listView.addItem(label)
        
        imagen = QImage(imagen_cv.data, imagen_cv.shape[1], imagen_cv.shape[0], QImage.Format_RGB888).rgbSwapped()
        pix = QPixmap.fromImage(imagen).scaled(700, 700, QtCore.Qt.KeepAspectRatio)
        self.ui.lbl_imagen.setPixmap(pix)
