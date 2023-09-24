from PyQt5.QtWidgets import QApplication,QGroupBox,QHBoxLayout,QTextBrowser,QMessageBox,QLabel,QDialog,QPushButton, QVBoxLayout, QLineEdit
import sys
from PyQt5 import QtGui
import sqlite3

class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.InitUI()
        

    def InitUI(self):
        self.setGeometry(100,100,300,400)
        self.setWindowIcon(QtGui.QIcon("home.png"))
        self.label_name=QLabel("Name?")
        self.label_id=QLabel("id?")
        
        self.lineedit_name=QLineEdit("")
        self.lineedit_id=QLineEdit("")
        
        self.btn=QPushButton("db입력")
        self.btn_show_db=QPushButton("보기")
        self.btn_del=QPushButton("지우기")
        self.qrs=QTextBrowser()
        vbox=QVBoxLayout()
        hbox=QHBoxLayout()
        vbox.addWidget(self.label_name)
        vbox.addWidget(self.lineedit_name)
        vbox.addWidget(self.label_id)
        vbox.addWidget(self.lineedit_id)
        gbox=QGroupBox()
        hbox.addWidget(self.btn)
        hbox.addWidget(self.btn_show_db)
        hbox.addWidget(self.btn_del)
        gbox.setLayout(hbox)
        vbox.addWidget(gbox)
        vbox.addWidget(self.qrs)
        self.setLayout(vbox)

        self.btn.clicked.connect(self.db_btn_click)
        
        self.btn_show_db.clicked.connect(self.show_db)
        self.btn_del.clicked.connect(self.delete_all)
    
    def delete_all(self):
        conn=sqlite3.connect('testdb.sqlite')
        with conn:
            cur=conn.cursor()
            sql='delete from person'
            cur.execute(sql)
            conn.commit

    def show_db(self):
        conn=sqlite3.connect('testdb.sqlite')
        with conn:
            cur=conn.cursor()
            cur.execute('select * from person')
            conn.commit()
            rows=cur.fetchall()
            txt=""
            for row in rows:
                txt+=(row[0]+" "+str(row[1])+'\n')
            self.qrs.setPlainText(txt)
        
    def db_btn_click(self):
        conn=sqlite3.connect('testdb.sqlite') #없으면 새로만듦
        with conn:
            cur=conn.cursor()
            cur.execute('''
            CREATE TABLE IF NOT EXISTS person (name TEXT, id INTEGER)
            ''')
            # print(type(self.lineedit_name.text()))
            # cur.execute("Insert into person(name, id) values ('%s', '%d')" %(''.join(self.lineedit_name.text()),''.join(int(self.lineedit_id.text()))))
            try:
                sql="Insert into person (name, id) values (?,?)"
                cur.execute(sql,(self.lineedit_name.text(),int(self.lineedit_id.text())))
                # QMessageBox.about(self,'입력성공','input good')
            
                conn.commit()
            except Exception as e:
                QMessageBox.about(self,'입력오류','input bad')
        
            # cur.execute('select * from person')
            # rows=cur.fetchall()
            # for row in rows:
            #         self.qrs.append(row[0]+" "+str(row[1]))

            # self.close
    

        
App=QApplication(sys.argv)
win=Window()
win.show()
sys.exit(App.exec())
