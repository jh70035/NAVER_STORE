from PyQt5.QtWidgets import QTabWidget, QDialog, QApplication, QWidget \
    ,QLabel,QLineEdit, QVBoxLayout, QGroupBox,QPushButton,QDialogButtonBox \
    ,QGroupBox,QListWidget, QCheckBox, QComboBox, QMenuBar,QAction,QMainWindow
import sys
from PyQt5 import QtGui

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUi()
    
    def InitUi(self):
        self.listwidget=QListWidget()
        li=['java','c++', 'c#']
        self.listwidget.insertItem(0,'C++')
        self.listwidget.insertItem(1,'PYthon')
        self.listwidget.insertItem(2,'C#')
        self.listwidget.clicked.connect(self.list_clicked)
        self.vbox=QVBoxLayout()
        self.label=QLabel("Language you selected")
        self.label.setFont(QtGui.QFont("sanserif",15))

        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.listwidget)
        self.setLayout(self.vbox)

    def list_clicked(self):
        item=self.listwidget.currentItem()
        self.label.setText(str(item.text()))

App=QApplication(sys.argv)
win=Window()
win.show()
App.exec()
