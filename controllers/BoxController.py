from PyQt5 import QtWidgets, QtCore
from templates.WidgetCourtImage import Ui_Form
from utils.xml import xml_update

class BoxWidget(QtWidgets.QDialog):
    def __init__(self, rad, path_xml, index, pix, func):
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.array_radios = [self.ui.radio_bttn_a,self.ui.radio_bttn_b, 
                            self.ui.radio_bttn_c, self.ui.radio_bttn_d, 
                            self.ui.radio_bttn_e, self.ui.radio_bttn_f ]
        if rad > 0 :
            self.array_radios[rad - 1].setChecked(True)

        self.path_xml = path_xml
        self.index = index
        self.func = func
        self.ui.radio_bttn_a.clicked.connect(lambda: self.updateXml(1))
        self.ui.radio_bttn_b.clicked.connect(lambda: self.updateXml(2))
        self.ui.radio_bttn_c.clicked.connect(lambda: self.updateXml(3))
        self.ui.radio_bttn_d.clicked.connect(lambda: self.updateXml(4))
        self.ui.radio_bttn_e.clicked.connect(lambda: self.updateXml(5))
        self.ui.radio_bttn_f.clicked.connect(lambda: self.updateXml(6))

        self.ui.lbl_imagen.setPixmap(pix)

        self.show()

    def updateXml(self, rad):
        
        value = ''
        if rad == 1:
            value = 'surgical'
        elif rad == 2:
            value = 'valve'
        elif rad == 3:
            value = 'cloth'
        elif rad == 4:
            value ='respirator'
        elif rad == 5:
            value = 'others'
        elif rad == 6:
            value ='none'
        
        xml_update(self.path_xml, self.index, value)
        self.func()


