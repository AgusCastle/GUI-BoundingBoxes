from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QImage, QIcon, QColor
from utils.opencv import *
from utils.xml import xml_annotation, xml_get_name
from utils.files import returnAllfilesbyType

from templates.boundingBoxesMain import MainView
from controllers.BoxController import BoxWidget

class MainViewController(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = MainView()
        self.ui.setupUi(self)

        # Variables locales
        self.ruta_imagen = ''
        self.ruta_xml = ''

        self.ui.bttn_selectimg.clicked.connect(lambda: self.abrirDirectorioxml())
        self.ui.bttn_boxes.clicked.connect(lambda: self.abrirDirectorioImg())

        self.ui.bttn_next.clicked.connect(lambda: self.changeImagen('>'))
        self.ui.bttn_prev.clicked.connect(lambda: self.changeImagen('<'))
        
        self.ui.listView.doubleClicked.connect(self.onCliked)


        self.ui.bttn_boxes.setEnabled(False)
        self.ui.bttn_prev.setEnabled(False)
        self.ui.bttn_next.setEnabled(False)

        self.show()

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
        self.ruta_imagen = self.folderimg + '/' + name
        self.ui.lbl_titulo.setText(name)
        self.ruta_xml = self.list_xml_paths[self.index]

        self.setBoxes()

    def onCliked(self, item):
        index = self.ui.listView.currentRow()
        
        h, w, imagen_cv = cutImageBox(self.ruta_imagen, self.imgdata['boxes'][index])
        imagen = QImage(imagen_cv.data.tobytes(), w, h, w * 3, QImage.Format_RGB888).rgbSwapped()
        pix = QPixmap.fromImage(imagen).scaled(450, 450, QtCore.Qt.KeepAspectRatio)

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


        self.uiBox = BoxWidget( rad, self.ruta_xml, index, pix, self.setBoxes)

    def abrirDirectorioxml(self):
        self.folderxml = str(QtWidgets.QFileDialog.getExistingDirectory(None, "Selecciona ubicacion de los xml"))
        if self.folderxml:
            self.list_xml_paths = returnAllfilesbyType(path= self.folderxml, tfile='xml')
            if len(self.list_xml_paths ) > 0:
                self.ui.lbl_rutai.setText('Encontrados: {}'.format(len(self.list_xml_paths)))
                self.ui.bttn_boxes.setEnabled(True)
            else:
                self.ui.lbl_rutai.setText('No hay XML')

    def abrirDirectorioImg(self):
        self.folderimg = str(QtWidgets.QFileDialog.getExistingDirectory(None, "Selecciona ubicacion de las imagenes"))

        if self.folderimg:
            self.index = 0

            name = xml_get_name(self.list_xml_paths[self.index])
            self.ruta_imagen = self.folderimg + '/' + name
            self.ui.lbl_titulo.setText(name)
            self.ruta_xml = self.list_xml_paths[self.index]
            
            self.ui.bttn_next.setEnabled(True)
            self.setBoxes()


    def abrirFotografia(self):
        filename =  QtWidgets.QFileDialog.getOpenFileName(None, 'Buscar Imagen', '.', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
        
        if filename[0]:
            self.ruta_imagen = filename[0]
            #imagen = QImage(self.ruta_imagen)
            #pix = QPixmap.fromImage(imagen).scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
            #self.ui.lbl_titulo.setText(filename[0])
            #self.ui.lbl_imagen.setPixmap(pix)
            imagen_cv = test(self.ruta_imagen)
            imagen = QImage(imagen_cv.data, imagen_cv.shape[1], imagen_cv.shape[0], QImage.Format_RGB888).rgbSwapped()
            pix = QPixmap.fromImage(imagen).scaled(1000, 1000, QtCore.Qt.KeepAspectRatio)
            self.ui.lbl_imagen.setPixmap(pix)
    
    def agregarBoxesImagenListView(self):

        filename =  QtWidgets.QFileDialog.getOpenFileName(None, 'Buscar xml', '.', 'Image Files (*.xml)')

        if filename[0]:
            self.ruta_xml = filename[0]
        else:
            return

        self.setBoxes()

    def setBoxes(self):
        self.ui.listView.clear()

        self.imgdata = xml_annotation(self.ruta_xml)

        imagen_cv, colors = setBoxesToImage(self.ruta_imagen, self.imgdata)

        count = 0
        for i, c in zip(self.imgdata['labels'], colors):
            label = QtWidgets.QListWidgetItem()
            color = QPixmap(10,10)
            color.fill(QColor(c[2], c[1], c[0]))
            label.setIcon(QIcon(color))
            label.setText(i + " " +str(count + 1))
            self.ui.listView.addItem(label)
            count += 1
        
        imagen = QImage(imagen_cv.data, imagen_cv.shape[1], imagen_cv.shape[0], QImage.Format_RGB888).rgbSwapped()
        pix = QPixmap.fromImage(imagen).scaled(1000, 1000, QtCore.Qt.KeepAspectRatio)
        self.ui.lbl_imagen.setPixmap(pix)
