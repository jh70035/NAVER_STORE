from PyQt5.QtWidgets import QToolBox, QWidget, QVBoxLayout,QLabel, \
    QApplication, QMenuBar, QMainWindow, QAction, qApp, QTextEdit \
        ,QFontDialog, QMessageBox
import sys
from PyQt5.QtGui import QIcon

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,400,300)
        self.setWindowTitle('QMenuBar')
        self.setWindowIcon(QIcon('home.png'))

        mainMenu=self.menuBar()
        fileMenu=mainMenu.addMenu("File")
        exitAction=QAction(QIcon('exit.png'),'exit',self)
        fileMenu.addAction(exitAction)
        exitAction.triggered.connect(self.exitTriggered)
        editMenu=mainMenu.addMenu("Edit")
        
        copyAction=QAction(QIcon('copy.png'),'copy',self)
        editMenu.addAction(copyAction)
        copyAction.triggered.connect(self.copyTriggered)

        fontAction=QAction(QIcon('font.png'),'font',self)
        editMenu.addAction(fontAction)
        fontAction.triggered.connect(self.fontTriggered)

        helpMenu=mainMenu.addMenu("Help")
        helpAction=QAction(QIcon('help.png'),'help',self)
        helpMenu.addAction(helpAction)
        choiceAction=QAction(QIcon('choice.png'), 'choice',self)
        helpMenu.addAction(choiceAction)
        choiceAction.triggered.connect(self.choiceFct)
        helpAction.triggered.connect(self.helpTriggered)

        
        toolbar=self.addToolBar('toolbar')
        toolbar.addAction(exitAction)
        toolbar.addAction(copyAction)
        toolbar.addAction(fontAction)
        toolbar.addAction(helpAction)        
        self.createTextEditor()
        self.show()

    def choiceFct(self):
        msessagebox=QMessageBox.question(self,'choice message', 'Do you like pyqt5',QMessageBox.Yes | QMessageBox.No)
        if msessagebox ==QMessageBox.Yes:
            self.textEditor.setText('Yes, you like pyqt5')
        if msessagebox ==QMessageBox.No:
            self.textEditor.setText("No, you don't")
    
    def helpTriggered(self):
        messagebox=QMessageBox.about(self, 'about message', \
            'this is simple editor')

    def fontTriggered(self):
        font, ok=QFontDialog.getFont()
        if ok:
            self.textEditor.setFont(font)

    def createTextEditor(self):
        self.textEditor=QTextEdit(self)
        self.setCentralWidget(self.textEditor)

    def copyTriggered(self):
        pass

    def exitTriggered(self):
        self.close()
    
if __name__=="__main__":
    App=QApplication(sys.argv)
    window=Window()
    sys.exit(App.exec())
