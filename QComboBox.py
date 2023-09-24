from PyQt5.QtWidgets import QTabWidget, QDialog, QApplication, QWidget \
    ,QLabel,QLineEdit, QVBoxLayout, QGroupBox,QPushButton,QDialogButtonBox \
    ,QGroupBox, QCheckBox, QComboBox, QMenuBar,QAction,QMainWindow
import sys

class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.InitUi()

    def InitUi(self):
        self.setGeometry(500,200,300,100)
        self.combo=QComboBox()
        li=['Java', "C++", "Python"]
        self.combo.addItems(li)
        self.combo.currentTextChanged.connect(self.comboChanged)
        self.label=QLabel("you've selected " +self.combo.currentText())
        self.btn=QPushButton("new dialog")
        self.btn.clicked.connect(self.btnClicked)

        vbox=QVBoxLayout()
        vbox.addWidget(self.combo)
        vbox.addWidget(self.label)
        vbox.addWidget(self.btn)
        self.setLayout(vbox)
    def btnClicked(self):
        dialog=QDialog(self)
        dialog.setModal(True)
        dialog.show()
        # dialog.exec()

    def comboChanged(self):
        # print(self.combo.currentText())
        self.label.setText("you've selected " +self.combo.currentText())

App=QApplication(sys.argv)
win=Window()
win.show()
App.exec()

        