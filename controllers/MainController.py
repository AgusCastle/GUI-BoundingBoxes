from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QIcon, QColor
from utils.opencv import *
from utils.xml import xml_annotation, xml_get_name
from utils.files import returnAllfilesbyType, imagenInapropiada, imagenSinObjetos

from templates.boundingBoxesMain import MainView
from controllers.BoxController import BoxWidget
from pathlib import Path
import platform
from natsort import natsorted, os_sorted, realsorted, humansorted


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

        self.ui.bttn_boxes.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.bttn_next.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.bttn_nopor.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.bttn_selectimg.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.ui.listView.setFocusPolicy(QtCore.Qt.NoFocus)

        self.show()

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Enter or event.key() == QtCore.Qt.Key.Key_Control:
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
            elif self.imgdata['labels'][index] == 'other':
                rad = 5
            elif self.imgdata['labels'][index] == 'none':
                rad = 6

            self.uiBox = BoxWidget(
                rad, self.ruta_xml, index, pix, self.setBoxes)

        if event.key() == QtCore.Qt.Key.Key_D:
            self.changeImagen('>')

        if event.key() == QtCore.Qt.Key.Key_A:
            self.changeImagen('<')

        if event.key() == QtCore.Qt.Key.Key_L:
            self.moverSinObjetos()

        if event.key() == QtCore.Qt.Key.Key_J:
            self.moverInapropiado()

    def moverInapropiado(self):

        if self.messageBoxQuestion("Esta imagen se ignorara como parte del dataset, ¿Realmente desea eliminarlo?", "Inapropiada"):
            imagenInapropiada(self.root, self.list_img_paths[self.index], self.list_xml_paths[self.index], str(
                Path(self.list_img_paths[self.index]).name), str(Path(self.list_xml_paths[self.index]).name))
            self.list_img_paths.pop(self.index)
            self.list_xml_paths.pop(self.index)

            self.index = self.index - 1

            if self.index <= 0:
                self.index = 0

            if self.index == len(self.list_img_paths) + 1:
                self.index = len(self.list_img_paths) - 1

            self.controllersBttns(self.index)
            name = xml_get_name(self.list_xml_paths[self.index])
            self.ruta_imagen = self.list_img_paths[self.index]
            self.ui.lbl_titulo.setText(name)
            self.ruta_xml = self.list_xml_paths[self.index]

            self.setBoxes()

    def moverSinObjetos(self):
        if self.messageBoxQuestion("Esta imagen se ignorara como parte del dataset, ¿Realmente desea eliminarlo?", "Error de deteccion"):
            imagenSinObjetos(self.root, self.list_img_paths[self.index], self.list_xml_paths[self.index], str(
                Path(self.list_img_paths[self.index]).name), str(Path(self.list_xml_paths[self.index]).name))
            self.list_img_paths.pop(self.index)
            self.list_xml_paths.pop(self.index)

            if self.index == 0:
                self.index = 0

            if self.index == len(self.list_img_paths) + 1:
                self.index = len(self.list_img_paths) - 1

            self.index = self.index - 1

            self.controllersBttns(self.index)
            name = xml_get_name(self.list_xml_paths[self.index])
            self.ruta_imagen = self.list_img_paths[self.index]
            self.ui.lbl_titulo.setText(name)
            self.ruta_xml = self.list_xml_paths[self.index]

            self.setBoxes()

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
        if op == '>' and self.index < len(self.list_img_paths):
            self.index += 1
        if op == '<' and self.index > 0:
            self.index -= 1

        if self.index >= 0 and self.index < len(self.list_img_paths):

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

        labels = {0: 'other', 1: 'cloth', 2: 'other', 3: 'none',
                  4: 'respirator', 5: 'surgical', 6: 'valve'}
        rad = 0
        if self.imgdata['labels'][index] == 5:
            rad = 1
        elif self.imgdata['labels'][index] == 6:
            rad = 2
        elif self.imgdata['labels'][index] == 1:
            rad = 3
        elif self.imgdata['labels'][index] == 4:
            rad = 4
        elif self.imgdata['labels'][index] == 0:
            rad = 5
        elif self.imgdata['labels'][index] == 3:
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
            self.root = str(p.parents[1])
            ruta_xmls = str(p.parents[1]) + '/annotations'
            self.list_xml_paths = returnAllfilesbyType(ruta_xmls, '.xml')
            if len(self.list_xml_paths) == 0:
                ruta_xmls = str(p.parents[1]) + '/Annotations'
                self.list_xml_paths = returnAllfilesbyType(ruta_xmls, '.xml')

            self.list_img_paths = returnAllfilesbyType(ruta_imagenes, '.jpg')
            self.list_img_paths.extend(
                returnAllfilesbyType(ruta_imagenes, '.png'))

            if platform.system() == 'Windows':
                wd_list = []
                for i in self.list_xml_paths:
                    wd_list.append(i.replace('\\', '/'))

                self.list_xml_paths = wd_list

                wd_list = []
                for i in self.list_img_paths:
                    wd_list.append(i.replace('\\', '/'))

                self.list_img_paths = wd_list

            self.list_img_paths = os_sorted(self.list_img_paths)
            self.list_xml_paths = os_sorted(self.list_xml_paths)

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
        labels = {0: 'other', 1: 'cloth', 2: 'other', 3: 'none',
                  4: 'respirator', 5: 'surgical', 6: 'valve'}
        self.imgdata = xml_annotation(self.ruta_xml)

        colors = setBoxesToImage(self.ruta_imagen, self.imgdata)
        count = 0
        for i, c in zip(self.imgdata['labels'], colors):
            label = QtWidgets.QListWidgetItem()
            color = QPixmap(10, 10)
            color.fill(QColor(c[2], c[1], c[0]))
            label.setIcon(QIcon(color))
            label.setText(labels[i] + " " + str(count + 1))
            self.ui.listView.addItem(label)
            count += 1
        pix = QPixmap('./img.jpg').scaled(
            1126, 632, QtCore.Qt.KeepAspectRatio)
        self.ui.lbl_imagen.setPixmap(pix)

    def messageBoxQuestion(self, message, title):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)

        # setting message for Message Box
        msg.setText(message)

        # setting Message box window title
        msg.setWindowTitle(title)

        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        ret_val = msg.exec_()

        if QMessageBox.Ok == ret_val:
            return True
        return False
