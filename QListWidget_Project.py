from PyQt5.QtWidgets import QTabWidget, QDialog, QApplication, QWidget \
    ,QLabel,QLineEdit,QMessageBox ,QVBoxLayout, QHBoxLayout,QGroupBox,QPushButton,QDialogButtonBox \
    ,QGroupBox,QListWidget,QWizard, QInputDialog,QCheckBox, QComboBox, QMenuBar,QAction,QMainWindow
import sys
from PyQt5 import QtGui

class Window(QWidget):
    def __init__(self, programming=None):
        super(Window,self).__init__()
        self.li=[]
        if programming is not None:
            self.li=programming
        self.InitUi()
    
    def InitUi(self):
        self.listwidget=QListWidget()
        # li=['java','c++', 'c#']
        # self.listwidget.insertItem(0,'C++')
        # self.listwidget.insertItem(1,'PYthon')
        # self.listwidget.insertItem(2,'C#')
        self.listwidget.addItems(self.li)
        self.listwidget.setCurrentRow(0)
        self.vbox=QVBoxLayout()
        self.vbox.addWidget(self.listwidget)
        self.vbox2=QVBoxLayout()
        for text, slot in (("Add", self.add), 
                           ("Edit", self.edit),
                           ("Remove", self.remove),
                           ("Sort", self.sort),
                           ("exit", self.exit)
                          ):
            btn=QPushButton(text)
            btn.clicked.connect(slot)
            self.vbox2.addWidget(btn)
        groubox=QGroupBox()
        vbox3=QVBoxLayout()
        wizardbtn=QPushButton("Launch wizard")
        vbox3.addWidget(wizardbtn)
        groubox.setLayout(vbox3)
        wizardbtn.clicked.connect(self.wizartBtnClicked)
        self.vbox2.addWidget(groubox)

        self.hbox=QHBoxLayout()
        self.hbox.addWidget(self.listwidget)
        self.hbox.addLayout(self.vbox2)
        self.setLayout(self.hbox)

        self.wizardwin=QWizard()
    
    def wizartBtnClicked(self):
        self.wizardwin.open()

    def sort(self):
        self.listwidget.sortItems()

    def add(self):
        string, ok=QInputDialog.getText(self,'Add Language','추가할 언어를 입력하세요')
        if ok and string is not None:
            row=self.listwidget.currentRow()
            self.listwidget.insertItem(row,string)


    def edit(self):
        row=self.listwidget.currentRow()
        item=self.listwidget.item(row)
        # string, ok=QInputDialog.getText(self,'Edit Language','Enter new Language',QLineEdit.Normal,item.text())
        string, ok=QInputDialog.getText(self,'Edit Language',f"{item.text()}(을)를 무엇으로 수정하시겠나요?")
        
        if ok and string is not None:  
            item.setText(string)

    def exit(self):
        self.close()

    def remove(self):
        row=self.listwidget.currentRow()
        item=self.listwidget.takeItem(row)
        del(item)
    


App=QApplication(sys.argv)
win=Window(['java','python','c++','ruby','kodlln'])
win.show()
App.exec()
