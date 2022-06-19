from importlib.resources import path
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QIcon, QColor
from utils.opencv import *
from utils.xml import xml_annotation, xml_get_name
from utils.files import returnAllfilesbyType

from templates.boundingBoxesMain import MainView
from controllers.BoxController import BoxWidget
from pathlib import Path


class MainViewController(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = MainView()
        self.ui.setupUi(self)

        # Variables locales
        self.ruta_imagen = ''
        self.ruta_xml = ''

        self.ui.bttn_selectimg.clicked.connect(
            lambda: self.abrirDirectorioxml())

        self.ui.bttn_next.clicked.connect(lambda: self.changeImagen('>'))
        self.ui.bttn_prev.clicked.connect(lambda: self.changeImagen('<'))
        self.ui.bttn_boxes.clicked.connect(lambda: self.moverSinObjetos())
        self.ui.bttn_nopor.clicked.connect(lambda: self.moverInapropiado())
        self.ui.listView.doubleClicked.connect(self.onCliked)

        self.ui.bttn_nopor.setEnabled(False)
        self.ui.bttn_boxes.setEnabled(False)
        self.ui.bttn_prev.setEnabled(False)
        self.ui.bttn_next.setEnabled(False)

        self.show()

    def moverInapropiado(self):

        if self.messageBoxQuestion("Esta imagen se ignorara como parte del dataset, ¿Realmente desea eliminarlo?"):
            print("Me la pelas")

    def moverSinObjetos(self):
        pass

    def controllersBttns(self, i):
        if i == (len(self.list_xml_paths) - 1):
            self.ui.bttn_next.setEnabled(False)
        else:
            self.ui.bttn_next.setEnabled(True)

        if i == 0:
            self.ui.bttn_prev.setEnabled(False)
        else:
            self.ui.bttn_prev.setEnabled(True)

    def changeImagen(self, op):

        if op == '>':
            self.index += 1
        if op == '<':
            self.index -= 1

        self.controllersBttns(self.index)
        name = xml_get_name(self.list_xml_paths[self.index])
        self.ruta_imagen = self.list_img_paths[self.index]
        self.ui.lbl_titulo.setText(name)
        self.ruta_xml = self.list_xml_paths[self.index]

        self.setBoxes()

    def onCliked(self, item):
        index = self.ui.listView.currentRow()

        h, w, imagen_cv = cutImageBox(
            self.ruta_imagen, self.imgdata['boxes'][index])
        imagen = QImage(imagen_cv.data.tobytes(), w, h, w *
                        3, QImage.Format_RGB888).rgbSwapped()
        pix = QPixmap.fromImage(imagen).scaled(
            450, 450, QtCore.Qt.KeepAspectRatio)

        rad = 0
        if self.imgdata['labels'][index] == 'surgical':
            rad = 1
        elif self.imgdata['labels'][index] == 'valve':
            rad = 2
        elif self.imgdata['labels'][index] == 'cloth':
            rad = 3
        elif self.imgdata['labels'][index] == 'respirator':
            rad = 4
        elif self.imgdata['labels'][index] == 'others':
            rad = 5
        elif self.imgdata['labels'][index] == 'none':
            rad = 6

        self.uiBox = BoxWidget(rad, self.ruta_xml, index, pix, self.setBoxes)

    def abrirDirectorioxml(self):

        path_img = QtWidgets.QFileDialog.getOpenFileName(
            None, 'Buscar Imagen', '.', 'Image Files (*.jpg *.png)')

        if path_img[0]:
            p = Path(path_img[0])
            # Imagen actual la cual despues se indexara
            self.ruta_imagen = path_img[0]
            # Ruta del directorio de las imagenes
            ruta_imagenes = str(p.parent)
            # Ruta del directorio de los XML
            ruta_xmls = str(p.parents[1]) + '/annotations'
            self.list_xml_paths = returnAllfilesbyType(ruta_xmls, '.xml')
            self.list_img_paths = returnAllfilesbyType(ruta_imagenes, '.jpg')
            self.list_img_paths.extend(
                returnAllfilesbyType(ruta_imagenes, '.png'))
            self.list_img_paths.sort()
            self.list_xml_paths.sort()

            if self.validarIntegridad(self.list_xml_paths, self.list_img_paths):
                self.index = self.list_img_paths.index(path_img[0])

                name = xml_get_name(self.list_xml_paths[self.index])
                self.ui.lbl_titulo.setText(name)

                self.ruta_imagen = self.list_img_paths[self.index]
                self.ruta_xml = self.list_xml_paths[self.index]

                self.ui.bttn_next.setEnabled(True)
                self.ui.bttn_prev.setEnabled(True)

                if self.index == 0:
                    self.ui.bttn_prev.setEnabled(False)
                elif self.index == len(self.list_img_paths) - 1:
                    self.ui.bttn_next.setEnabled(False)

                self.ui.bttn_nopor.setEnabled(True)
                self.ui.bttn_boxes.setEnabled(True)
                self.setBoxes()

    def validarIntegridad(self, list_xml, list_img):

        if len(list_xml) != len(list_img):
            QtWidgets.QMessageBox.about(
                self, "Mucho ojo", "No hay el mismo numero de imagenes que de xml en tus carpetas revisa eso")
            return False

        def getNombresArchivos(vector):
            nombres = []
            for path in vector:
                p = Path(path)
                nombres.append(str(p.stem))
            return nombres

        for xml, img in zip(getNombresArchivos(list_xml), getNombresArchivos(list_img)):
            if xml != img:
                QtWidgets.QMessageBox.about(
                    self, "Mucho ojo", "Hay algunos xml o imagenes que no coinciden checalos")
                return False
        return True

    def abrirFotografia(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(
            None, 'Buscar Imagen', '.', 'Image Files (*.png *.jpg *.jpeg *.bmp)')

        if filename[0]:
            self.ruta_imagen = filename[0]
            #imagen = QImage(self.ruta_imagen)
            #pix = QPixmap.fromImage(imagen).scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
            # self.ui.lbl_titulo.setText(filename[0])
            # self.ui.lbl_imagen.setPixmap(pix)
            imagen_cv = test(self.ruta_imagen)
            imagen = QImage(
                imagen_cv.data, imagen_cv.shape[1], imagen_cv.shape[0], QImage.Format_RGB888).rgbSwapped()
            pix = QPixmap.fromImage(imagen).scaled(
                1000, 1000, QtCore.Qt.KeepAspectRatio)
            self.ui.lbl_imagen.setPixmap(pix)

    def setBoxes(self):
        self.ui.listView.clear()

        self.imgdata = xml_annotation(self.ruta_xml)

        imagen_cv, colors = setBoxesToImage(self.ruta_imagen, self.imgdata)

        count = 0
        for i, c in zip(self.imgdata['labels'], colors):
            label = QtWidgets.QListWidgetItem()
            color = QPixmap(10, 10)
            color.fill(QColor(c[2], c[1], c[0]))
            label.setIcon(QIcon(color))
            label.setText(i + " " + str(count + 1))
            self.ui.listView.addItem(label)
            count += 1

        imagen = QImage(
            imagen_cv.data, imagen_cv.shape[1], imagen_cv.shape[0], QImage.Format_RGB888).rgbSwapped()
        pix = QPixmap.fromImage(imagen).scaled(
            854, 480, QtCore.Qt.KeepAspectRatio)
        self.ui.lbl_imagen.setPixmap(pix)

    def messageBoxQuestion(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)

        # setting message for Message Box
        msg.setText(message)

        # setting Message box window title
        msg.setWindowTitle("Advertencia")

        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        ret_val = msg.exec_()

        if QMessageBox.Ok == ret_val:
            return True
        return False
