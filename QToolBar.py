from PyQt5.QtWidgets import QApplication, QMenuBar, QMainWindow \
    ,QAction
import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left=100
        self.top=100
        self.width=400
        self.height=300
        self.iconName="home.png"
        self.title = "QToolBar"
        self.initWindow()

        self.show()

    def initWindow(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon(self.iconName))
        self.setWindowTitle(self.title)
        mainMenu=self.menuBar()
        fileMenu=mainMenu.addMenu("File")
        copyAction=QAction(QIcon("copy.png"),"copy",self)
        fileMenu.addAction(copyAction)
        copyAction.triggered.connect(self.copyTriggered)
    
    def copyTriggered(self):
        self.close()

App=QApplication(sys.argv)
win=Window()
sys.exit(App.exec())

