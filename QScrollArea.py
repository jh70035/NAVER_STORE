from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox \
    , QFormLayout, QLabel, QPushButton, QVBoxLayout,QScrollArea
import sys

class Window(QWidget):
    def __init__(self,val):
        super().__init__()
        self.left=100
        self.top=100
        self.width=400
        self.height=1000
        self.InitWindow()
        self.val=val

    def InitWindow(self):
        self.groupbox=QGroupBox("This is a group box")
        self.formlayout=QFormLayout()
        listLabels=[]
        listButtons=[]
        for i in range(30):
            listLabels.append(QLabel("This is a label"))
            listButtons.append(QPushButton("click me"))
            self.formlayout.addRow(listLabels[i], listButtons[i])

        self.groupbox.setLayout(self.formlayout)
        self.scrollarea=QScrollArea()
        
        self.scrollarea.setWidget(self.groupbox)
        
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setFixedHeight(400)

        vbox=QVBoxLayout()
        vbox.addWidget(self.scrollarea)
        self.setLayout(vbox)
        self.show()

if __name__=="__main__":
    App=QApplication(sys.argv)
    window=Window(10)
    sys.exit(App.exec())
