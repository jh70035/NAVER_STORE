from PyQt5.QtWidgets import QTabWidget, QDialog, QApplication, QWidget \
    ,QLabel,QLineEdit, QVBoxLayout,QHBoxLayout ,QGroupBox,QPushButton,QDialogButtonBox \
    ,QGroupBox, QFileDialog,QInputDialog,QCheckBox,QTableWidget,QTableWidgetItem,QComboBox,QListWidget ,QMenuBar,QAction,QMainWindow
import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5 import Qt
import requests
from bs4 import BeautifulSoup
from functools import partial
import sqlite3
from datetime import datetime, timedelta
from save_prod_list_db import all_items

from PyQt5.QtChart import QChart, QChartView, QLineSeries, QDateTimeAxis
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter


from PyQt5.QtCore import QDate, QDateTime

from PyQt5.QtCore import *
from navershopping import find_item2

class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,800,800)
        self.initWindow()

    def initWindow(self):
    
        vbox=QVBoxLayout()
        tabwidget=QTabWidget()
        tabwidget.addTab(MyStorFarm(), "나의 스토어팜")
        tabwidget.addTab(ProdDetail(), "개별상품 분석")
        tabwidget.addTab(TabKeyword(), "키워드분석")
        tabwidget.addTab(ContactDetail(),"신상품 찾기")
        tabwidget.addTab(ImageLoad(), "트렌트분석")
        
        # self.buttonbox=QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        # self.buttonbox.accepted.connect(self.acc)
        # self.buttonbox.rejected.connect(self.rej)

        vbox.addWidget(tabwidget)
        # vbox.addWidget(self.buttonbox)
        self.setLayout(vbox)

    def acc(self):
        self.close()
    def rej(self):
        pass

class FarmList(QWidget):
    def __init__(self,li):
        super().__init__()
        self.InitUi(li)
        self.farmlist=li
    
    def InitUi(self):
        self.listwidget=QListWidget()
        self.listwidget.addItems(self.farmlist)
        self.hbox=QHBoxLayout()
        self.addBtn=QPushButton('add')

        self.hbox.addWidget(self.listwidget)
        self.hbox.addWidget(self.addBtn)
        
        self.addBtn.clicked.connect(partial(self.addFarm,self.farmlist))
        self.setLayout(self.hbox)

    def addFarm(self,li):
        string, ok=QInputDialog.getText(self,'Add Farm','추가할 스토어팜 주소를 입력하세요')
        if ok and string is not None:
            row=self.listwidget.currentRow()
            self.listwidget.insertItem(row,string)
            li.append(string)
            print(li)

    # def list_clicked(self):
    #     item=self.listwidget.currentItem()
    #     self.label.setText(str(item.text()))

class ProdDetail(QWidget):
    def __init__(self):
        super().__init__()
        hbox=QHBoxLayout()
        hbox2=QHBoxLayout()
        hbox3=QHBoxLayout()
        hbox4=QHBoxLayout()

        self.prod_combo=QComboBox()
        self.lineEditProdName=QLineEdit()
        namelabel=QLabel("스토어팜주소")
        self.farm_combo=QComboBox()
        self.li=['https://smartstore.naver.com/heyhannah','https://smartstore.naver.com/monsclub']
        self.farm_combo.addItems(self.li)
        self.shop_title_label=QLabel()
        self.show_farm_name()
        self.btn_show_prod_detail=QPushButton('조회')
        self.btn_show_prod_detail.setIcon(QtGui.QIcon('update.png'))

        hbox.addWidget(namelabel)
        hbox.addWidget(self.farm_combo)
        hbox.addWidget(self.shop_title_label)

        hbox2.addWidget(QLabel("상품명"))
        hbox2.addWidget(self.prod_combo)
        
        hbox2.addStretch()
        hbox3.addWidget(QLabel("직접입력"))
        

        hbox3.addWidget(self.lineEditProdName)
        hbox3.addWidget(self.btn_show_prod_detail)
        hbox3.addStretch()

        self.init_prod_combo()
        self.btn_show_prod_detail.clicked.connect(self.get_prod_detail)
        self.farm_combo.currentTextChanged.connect(self.show_farm_name)
        self.prod_combo.currentTextChanged.connect(self.input_prod_title)

        vbox=QVBoxLayout()
   
        self.linechart=QChart()
        self.linechart2=QChart()
        self.linechart3=QChart()
        
        self.chartview = QChartView(self.linechart)
        self.chartview2 = QChartView(self.linechart2)
        self.chartview3 = QChartView(self.linechart3)

        self.tablewidget=QTableWidget()

        self.chartgroup=QGroupBox()
        self.chartvbox=QVBoxLayout()
        self.chartvbox.addWidget(self.chartview)
        self.chartvbox.addWidget(self.chartview2)
        self.chartvbox.addWidget(self.chartview3)
        
        self.chartgroup.setLayout(self.chartvbox)

        hbox4.addWidget(self.tablewidget)
        # hbox4.addWidget(self.chartview)
        hbox4.addWidget(self.chartgroup)

        self.updateProdDetail()
        self.groupbox=QGroupBox()
        self.groupbox2=QGroupBox()
        self.groupbox3=QGroupBox()
        self.groupbox4=QGroupBox()

        self.groupbox.setLayout(hbox)
        self.groupbox2.setLayout(hbox2)
        self.groupbox3.setLayout(hbox3)
        self.groupbox4.setLayout(hbox4)
        
        vbox.addWidget(self.groupbox)
        vbox.addWidget(self.groupbox2)
        vbox.addWidget(self.groupbox3)
        vbox.addWidget(self.groupbox4)
        
        self.setLayout(vbox)

    def init_prod_combo(self):
        mall_url=self.farm_combo.currentText()
        conn=sqlite3.connect('emaildb.sqlite')
        cur=conn.cursor()
        sql=f"Select distinct title from PROD3 where link like '{mall_url}%'"
 
        cur.execute(sql)
        conn.commit()
        
        rows=cur.fetchall()

        li=[]
        for row in rows:
            li.append(row[0])
 
        self.prod_combo.clear()
        self.prod_combo.addItems(li)

        cur.close()
        conn.close()
        self.lineEditProdName.setText(self.prod_combo.currentText())

    def drawChart(self):
        conn=sqlite3.connect('emaildb.sqlite')
        cur=conn.cursor()

        title=self.lineEditProdName.text()
        mall_url=self.farm_combo.currentText()
        sql=f"select dt, jjim, sold, review from PROD3 where title='{title}'"
        cur.execute(sql)
        conn.commit()
        rows=cur.fetchall()
        series=[]
        # series = QLineSeries(self)
        series.append(QLineSeries(self))
        series.append(QLineSeries(self))
        series.append(QLineSeries(self))
        
        tod=datetime.today()
        nextday=datetime.today()+timedelta(days=1)
        d=QDate(2020,1,3)
        dt=QDateTime(d)
        d2=d.addDays(1)
        dt2=dt.addDays(1)

        for i,row in enumerate(rows):
            for j, serie in enumerate(series):
                # serie.append((dt.addDays(i)).toMSecsSinceEpoch(),int(row[j+1]))
                serie.append(i,int(row[j+1]))

        for serie in series:
            serie.setPointsVisible(True)
            
        self.linechart.removeAllSeries()
        self.linechart2.removeAllSeries()
        self.linechart3.removeAllSeries()
        

        self.linechart.addSeries(series[0])
        self.linechart2.addSeries(series[1])
        self.linechart3.addSeries(series[2])
        
        dateAxis=QDateTimeAxis()
        dateAxis2=QDateTimeAxis()
        dateAxis3=QDateTimeAxis()
        
        self.linechart.addAxis(dateAxis, Qt.AlignBottom)
        self.linechart2.addAxis(dateAxis2, Qt.AlignBottom)
        self.linechart3.addAxis(dateAxis3, Qt.AlignBottom)
        
        self.linechart.createDefaultAxes()
        self.linechart2.createDefaultAxes()
        self.linechart3.createDefaultAxes()
                   
        self.linechart.setAnimationOptions(QChart.SeriesAnimations)
        self.linechart.setTitle("찜")
        self.linechart.legend().setVisible(True)

        self.linechart2.setAnimationOptions(QChart.SeriesAnimations)
        self.linechart2.setTitle("구매")
        self.linechart2.legend().setVisible(True)

        self.linechart3.setAnimationOptions(QChart.SeriesAnimations)
        self.linechart3.setTitle("리뷰")
        self.linechart3.legend().setVisible(True)


        self.chartview.setRenderHint(QPainter.Antialiasing)
        self.chartview2.setRenderHint(QPainter.Antialiasing)
        self.chartview3.setRenderHint(QPainter.Antialiasing)

        cur.close()
        conn.close()
        
    def updateProdDetail(self):
        self.tablewidget.clear()
        self.tablewidget.setRowCount(300)
        self.tablewidget.setColumnCount(6)
        self.tablewidget.setItem(0,0,QTableWidgetItem("날짜"))
        self.tablewidget.setItem(0,1,QTableWidgetItem("찜"))
        self.tablewidget.setItem(0,2,QTableWidgetItem("구매"))
        self.tablewidget.setItem(0,3,QTableWidgetItem("리뷰"))

        conn=sqlite3.connect('emaildb.sqlite')
        cur=conn.cursor()

        title=self.lineEditProdName.text()

        mall_url=self.farm_combo.currentText()
        sql=f"Select dt, jjim, sold, review from PROD3 where title='{title}' order by dt desc"

        cur.execute(sql)
        conn.commit()
        
        rows=cur.fetchall()

        for i,row in enumerate(rows):
            # print(i, row[0])
            for j, elem in enumerate(row):
                
            #     print(i+1,j,elem)
            #     self.tablewidget.setItem(i+1,j,QTableWidgetItem(elem))
                self.tablewidget.setItem(i+1,j,QTableWidgetItem(str(row[j])))
            # print(row[1])
                # self.tablewidget.setItem(i+1,1,QTableWidgetItem(str(row[1])))
                
        self.tablewidget.resizeColumnToContents(0)
        cur.close()
        conn.close()

        return len(rows)
    def input_prod_title(self):
        self.lineEditProdName.setText(self.prod_combo.currentText())

    def get_prod_detail(self):
        url=self.farm_combo.currentText()
        prod_title=self.lineEditProdName.text()
        self.tablewidget.clear()
        self.updateProdDetail()
        self.drawChart()

    def setFarm(self,li):
        self.farmlist=FarmList(self.li)
        # print(self.li)
        # self.farm_combo.addItems(self.li)
        self.farmlist.show()
        
    def show_farm_name(self):
        '''스토어팜 주소를 콤보박스에서 변경시에 검색하여 스토어팜 이름 표시
        prod_combo도 변경함
        '''
        # self.shop_title_label.setText("sssss")
        url=self.farm_combo.currentText()
        req=requests.get(url)
        soup=BeautifulSoup(req.text, 'html.parser')
        self.shop_title_label.setText(soup.find('title').text.strip())
        self.init_prod_combo()

        # self.init_prod_combo()
        # self.tablewidget.clear()
        # self.shop_title_label.setText("aaa")

class TabKeyword(QWidget):
    def __init__(self):
        super().__init__()
        hbox=QHBoxLayout()
        hbox2=QHBoxLayout()
        hbox3=QHBoxLayout()
        hbox4=QHBoxLayout()

        self.prod_combo=QComboBox()
        self.lineEditProdName=QLineEdit()
        namelabel=QLabel("스토어팜주소")
        self.farm_combo=QComboBox()
        self.li=['https://smartstore.naver.com/heyhannah','https://smartstore.naver.com/monsclub']
        self.farm_combo.addItems(self.li)
        self.shop_title_label=QLabel()
        self.show_farm_name()
        self.btn_show_prod_detail=QPushButton('조회')
        self.btn_update_keyword=QPushButton('키워드 업데이트')
        self.btn_show_prod_detail.setIcon(QtGui.QIcon('update.png'))
        self.btn_update_keyword.setIcon(QtGui.QIcon('update-tag.png'))

        hbox.addWidget(namelabel)
        hbox.addWidget(self.farm_combo)
        hbox.addWidget(self.shop_title_label)
        hbox.addWidget(self.btn_update_keyword)

        hbox2.addWidget(QLabel("키워드"))
        hbox2.addWidget(self.prod_combo)
        
        hbox2.addStretch()
        hbox3.addWidget(QLabel("직접입력"))
        

        hbox3.addWidget(self.lineEditProdName)
        hbox3.addWidget(self.btn_show_prod_detail)
        hbox3.addStretch()

        self.init_prod_combo()
        self.btn_show_prod_detail.clicked.connect(self.get_prod_detail)
        self.btn_update_keyword.clicked.connect(self.update_keyword)

        self.farm_combo.currentTextChanged.connect(self.show_farm_name)
        self.prod_combo.currentTextChanged.connect(self.input_prod_title)

        vbox=QVBoxLayout()
   
        self.linechart=QChart()
        self.linechart2=QChart()
        self.linechart3=QChart()
        
        self.chartview = QChartView(self.linechart)
        self.chartview2 = QChartView(self.linechart2)
        self.chartview3 = QChartView(self.linechart3)

        self.tablewidget=QTableWidget()

        self.chartgroup=QGroupBox()
        self.chartvbox=QVBoxLayout()
        self.chartvbox.addWidget(self.chartview)
        self.chartvbox.addWidget(self.chartview2)
        self.chartvbox.addWidget(self.chartview3)
        
        self.chartgroup.setLayout(self.chartvbox)

        hbox4.addWidget(self.tablewidget)
        # hbox4.addWidget(self.chartview)
        hbox4.addWidget(self.chartgroup)

        self.updateProdDetail()
        self.groupbox=QGroupBox()
        self.groupbox2=QGroupBox()
        self.groupbox3=QGroupBox()
        self.groupbox4=QGroupBox()

        self.groupbox.setLayout(hbox)
        self.groupbox2.setLayout(hbox2)
        self.groupbox3.setLayout(hbox3)
        self.groupbox4.setLayout(hbox4)
        
        vbox.addWidget(self.groupbox)
        vbox.addWidget(self.groupbox2)
        vbox.addWidget(self.groupbox3)
        vbox.addWidget(self.groupbox4)
        
        self.setLayout(vbox)


    def update_keyword(self):
        mall_url=self.farm_combo.currentText()
        conn=sqlite3.connect('emaildb.sqlite')
        cur=conn.cursor()
        sql=f"Select distinct pid from PROD3 where link like '{mall_url}%'"
 
        cur.execute(sql)
        conn.commit()
        
        rows=cur.fetchall()

        li_pid=[]
        for row in rows:
            li_pid.append(row[0])

        
        # self.prod_combo.clear()
        # self.prod_combo.addItems(li)

        # cur.close()
        # conn.close()
        # self.lineEditProdName.setText(self.prod_combo.currentText())


    def init_prod_combo(self):
        mall_url=self.farm_combo.currentText()
        conn=sqlite3.connect('emaildb.sqlite')
        cur=conn.cursor()
        # sql=f"Select distinct keyword from KEYWORD where link like '{mall_url}%'"
        sql=f"Select distinct keyword from KEYWORD"
 
        cur.execute(sql)
        conn.commit()
        
        rows=cur.fetchall()

        li=[]
        for row in rows:
            li.append(row[0])
 
        self.prod_combo.clear()
        self.prod_combo.addItems(li)

        cur.close()
        conn.close()
        self.lineEditProdName.setText(self.prod_combo.currentText())

    def drawChart(self):
        conn=sqlite3.connect('emaildb.sqlite')
        cur=conn.cursor()

        title=self.lineEditProdName.text()
        mall_url=self.farm_combo.currentText()
        sql=f"select dt, jjim, sold, review from PROD3 where title='{title}'"
        cur.execute(sql)
        conn.commit()
        rows=cur.fetchall()
        series=[]
        # series = QLineSeries(self)
        series.append(QLineSeries(self))
        series.append(QLineSeries(self))
        series.append(QLineSeries(self))
        
        tod=datetime.today()
        nextday=datetime.today()+timedelta(days=1)
        d=QDate(2020,1,3)
        dt=QDateTime(d)
        d2=d.addDays(1)
        dt2=dt.addDays(1)

        for i,row in enumerate(rows):
            for j, serie in enumerate(series):
                # serie.append((dt.addDays(i)).toMSecsSinceEpoch(),int(row[j+1]))
                serie.append(i,int(row[j+1]))

        for serie in series:
            serie.setPointsVisible(True)
            
        self.linechart.removeAllSeries()
        self.linechart2.removeAllSeries()
        self.linechart3.removeAllSeries()
        

        self.linechart.addSeries(series[0])
        self.linechart2.addSeries(series[1])
        self.linechart3.addSeries(series[2])
        
        dateAxis=QDateTimeAxis()
        dateAxis2=QDateTimeAxis()
        dateAxis3=QDateTimeAxis()
        
        self.linechart.addAxis(dateAxis, Qt.AlignBottom)
        self.linechart2.addAxis(dateAxis2, Qt.AlignBottom)
        self.linechart3.addAxis(dateAxis3, Qt.AlignBottom)
        
        self.linechart.createDefaultAxes()
        self.linechart2.createDefaultAxes()
        self.linechart3.createDefaultAxes()
                   
        self.linechart.setAnimationOptions(QChart.SeriesAnimations)
        self.linechart.setTitle("찜")
        self.linechart.legend().setVisible(True)

        self.linechart2.setAnimationOptions(QChart.SeriesAnimations)
        self.linechart2.setTitle("구매")
        self.linechart2.legend().setVisible(True)

        self.linechart3.setAnimationOptions(QChart.SeriesAnimations)
        self.linechart3.setTitle("리뷰")
        self.linechart3.legend().setVisible(True)


        self.chartview.setRenderHint(QPainter.Antialiasing)
        self.chartview2.setRenderHint(QPainter.Antialiasing)
        self.chartview3.setRenderHint(QPainter.Antialiasing)

        cur.close()
        conn.close()
        
    def updateProdDetail(self):
        self.tablewidget.clear()
        self.tablewidget.setRowCount(300)
        self.tablewidget.setColumnCount(6)
        self.tablewidget.setItem(0,0,QTableWidgetItem("키워드"))
        self.tablewidget.setItem(0,1,QTableWidgetItem("상품명"))
        self.tablewidget.setItem(0,2,QTableWidgetItem("네이버검색페이지"))
        self.tablewidget.setItem(0,3,QTableWidgetItem("순번"))

        # conn=sqlite3.connect('emaildb.sqlite')
        # cur=conn.cursor()

        # title=self.lineEditProdName.text()

        # mall_url=self.farm_combo.currentText()
        # sql=f"Select dt, jjim, sold, review from PROD3 where title='{title}' order by dt desc"

        # cur.execute(sql)
        # conn.commit()
        
        # rows=cur.fetchall()
        keyword=self.lineEditProdName.text()
        mall_name=''

        rs=find_item2(keyword,mall_name)
        
        # for i,row in enumerate(rows):
        #     # print(i, row[0])
        #     for j, elem in enumerate(row):
                
        #     #     print(i+1,j,elem)
        #     #     self.tablewidget.setItem(i+1,j,QTableWidgetItem(elem))
        #         self.tablewidget.setItem(i+1,j,QTableWidgetItem(str(row[j])))
        #     # print(row[1])
        #         # self.tablewidget.setItem(i+1,1,QTableWidgetItem(str(row[1])))
                
        # self.tablewidget.resizeColumnToContents(0)
        # cur.close()
        # conn.close()

        # return len(rows)
    def input_prod_title(self):
        self.lineEditProdName.setText(self.prod_combo.currentText())

    def get_prod_detail(self):
        url=self.farm_combo.currentText()
        prod_title=self.lineEditProdName.text()
        self.tablewidget.clear()
        self.updateProdDetail()
        self.drawChart()

    def setFarm(self,li):
        self.farmlist=FarmList(self.li)
        # print(self.li)
        # self.farm_combo.addItems(self.li)
        self.farmlist.show()
        
    def show_farm_name(self):
        '''스토어팜 주소를 콤보박스에서 변경시에 검색하여 스토어팜 이름 표시
        prod_combo도 변경함
        '''
        # self.shop_title_label.setText("sssss")
        url=self.farm_combo.currentText()
        req=requests.get(url)
        soup=BeautifulSoup(req.text, 'html.parser')
        self.shop_title_label.setText(soup.find('title').text.strip())
        self.init_prod_combo()

        # self.init_prod_combo()
        # self.tablewidget.clear()
        # self.shop_title_label.setText("aaa")

class MyStorFarm(QWidget):
    def __init__(self):
        super().__init__()
        hbox=QHBoxLayout()
        hbox2=QHBoxLayout()
        namelabel=QLabel("스토어팜주소")
        self.farm_combo=QComboBox()
        self.li=['https://smartstore.naver.com/heyhannah','https://smartstore.naver.com/monsclub']
        self.farm_combo.addItems(self.li)
        self.shop_title_label=QLabel()
        self.show_farm_name()
        self.btn_show_prod=QPushButton('조회')
        self.btn_show_prod.setIcon(QtGui.QIcon('update.png'))
        self.gear_btn=QPushButton()
        self.gear_btn.setIcon(QtGui.QIcon('gear.png'))

        hbox.addWidget(namelabel)
        hbox.addWidget(self.farm_combo)
        hbox.addWidget(self.shop_title_label)
        hbox.addWidget(self.btn_show_prod)
        # hbox.addWidget(self.gear_btn)

        self.date_combo=QComboBox()
        self.init_date_combo()
        self.btn_download=QPushButton("금일 데이터 받기")
        self.btn_download.setIcon(QtGui.QIcon("download.png"))
        hbox2.addWidget(QLabel("조회일"))
        hbox2.addWidget(self.date_combo)
        hbox2.addWidget(self.btn_download)
        hbox2.addStretch()
        self.gear_btn.clicked.connect(partial(self.setFarm,self.li))
        self.btn_show_prod.clicked.connect(self.get_prod)
        self.farm_combo.currentTextChanged.connect(self.show_farm_name)
        self.btn_download.clicked.connect(self.download_data)
        vbox=QVBoxLayout()
        self.tablewidget=QTableWidget()

        self.updateProdList()
        self.groupbox=QGroupBox()
        self.groupbox2=QGroupBox()
        self.groupbox.setLayout(hbox)
        self.groupbox2.setLayout(hbox2)
    
        vbox.addWidget(self.groupbox)
        vbox.addWidget(self.groupbox2)
        
        self.tablewidget.resizeColumnToContents(0)
        vbox.addWidget(self.tablewidget)
        
        self.setLayout(vbox)
    
    def download_data(self):
        # mall_name='헤이해나'
        mall_name=self.shop_title_label.text()
        url_home=self.farm_combo.currentText()
        # req=requests.get(url)
        # soup=BeautifulSoup(req.text, 'html.parser')
        # self.shop_title_label.setText(soup.find('title').text.strip())


        itemslist=all_items(mall_name, url_home)
        
        # print(itemslist)
        conn=sqlite3.connect('emaildb.sqlite')
        cur=conn.cursor()
        tod=datetime.today()+timedelta(days=0)
        tod=tod.strftime('%Y-%m-%d')
        
        url_home=self.farm_combo.currentText()
        # print(tod)
        for item in itemslist:
            #update link
            item['link']=url_home+'/products/'+item['pid']
            # link=url_home="https://smartstore.naver.com/heyhannah/products/" +pid
            # print(item['name'])
            sql=f"REPLACE INTO PROD3 (dt,title, pid,jjim, sold,review,link) VALUES('{tod}','{item['name']}','{item['pid']}','{item['jjim']}','{item['sold']}','{item['review']}','{item['link']}')"
            # print(sql)
            cur.execute(sql)
            # cur.execute('''
            #         REPLACE INTO PROD3 (dt,title, pid,jjim, sold,review,link) VALUES (?,?,?,?,?,?,?);''', (tod,item['name'],item['pid'],item['jjim'],item['sold'],item['review']))
            conn.commit()
        # conn.commit()
        cur.close()
        conn.close()
        self.init_date_combo()
        self.updateProdList()

    def init_date_combo(self):
        mall_url=self.farm_combo.currentText()
        conn=sqlite3.connect('emaildb.sqlite')
        cur=conn.cursor()
        # tod=datetime.today().strftime('%Y-%m-%d')

        # for item in itemslist:
        #     cur.execute('''
        #             REP
        # lACE INTO PROD (dt,title, pid, jjim, sold,review) VALUES (?,?,?,?,?,?);''', (tod,item['name'],item['pid'] ,item['jjim'],item['sold'],item['review']))
        sql=f"Select distinct dt from PROD3 where link like '{mall_url}%'"

        cur.execute(sql)
        conn.commit()
        
        rows=cur.fetchall()

        
        li=[]
        for row in rows:
            li.append(row[0])
        # tod=datetime.today().strftime('%Y-%m-%d')
        # if tod not in li:
        #     li.append(tod)
        
        li.sort(reverse=True)
        self.date_combo.clear()
        self.date_combo.addItems(li)
        # rs=self.updateProdList()
        # print(rs)
        cur.close()
        conn.close()
        # print(li)

    def updateProdList(self):
        self.tablewidget.clear()
        self.tablewidget.setRowCount(300)
        self.tablewidget.setColumnCount(6)
        self.tablewidget.setItem(0,0,QTableWidgetItem("상품명"))
        self.tablewidget.setItem(0,1,QTableWidgetItem("찜"))
        self.tablewidget.setItem(0,2,QTableWidgetItem("구매"))
        self.tablewidget.setItem(0,3,QTableWidgetItem("리뷰"))
        self.tablewidget.setItem(0,4,QTableWidgetItem("LINK"))
        
        

        # itemslist=all_items()
        conn=sqlite3.connect('emaildb.sqlite')
        cur=conn.cursor()
        # tod=datetime.today().strftime('%Y-%m-%d')
        dateToSearch=self.date_combo.currentText()
        dateBefore=1
        sql=f"select distinct dt from PROD3;"
        cur.execute(sql)
        conn.commit()
        rows=cur.fetchall()
        row0=rows[0][0]
        print(row0)
        print(type(row0))

        mall_url=self.farm_combo.currentText()
        # for item in itemslist:
        #     cur.execute('''
        #             REPlACE INTO PROD (dt,title, pid, jjim, sold,review) VALUES (?,?,?,?,?,?);''', (tod,item['name'],item['pid'] ,item['jjim'],item['sold'],item['review']))
        
        # cur.execute('''
        #             Select title, jjim, sold, review from PROD3 where dt='2020-04-14' order by sold desc ''')
        # sql=f"Select title, jjim, sold, review,link from PROD3 where dt='{tod}' and link like '{self.farm_combo.currentText()}%'order by sold desc"
        sql=f"Select title, jjim, sold, review,link from PROD3 where dt='{dateToSearch}' and link like '{mall_url}%'  order by sold desc"
        cur.execute(sql)
        conn.commit()
        rows=cur.fetchall()
        

        for i,row in enumerate(rows):
            # print(i, row[0])
            for j, elem in enumerate(row):
                
            #     print(i+1,j,elem)
            #     self.tablewidget.setItem(i+1,j,QTableWidgetItem(elem))
                self.tablewidget.setItem(i+1,j,QTableWidgetItem(str(row[j])))
            # print(row[1])
                # self.tablewidget.setItem(i+1,1,QTableWidgetItem(str(row[1])))
                
        self.tablewidget.resizeColumnToContents(0)
        cur.close()
        conn.close()

        return len(rows)

    def get_prod(self):
        url=self.farm_combo.currentText()
        dt=self.date_combo.currentText()
        self.tablewidget.clear()
        self.updateProdList()
        # print(url)
        

    def setFarm(self,li):
        self.farmlist=FarmList(self.li)
        # print(self.li)
        # self.farm_combo.addItems(self.li)
        self.farmlist.show()
        
    def show_farm_name(self):
        '''스토어팜 주소를 콤보박스에서 변경시에 검색하여 스토어팜 이름 표시
        date_combo도 변경함
        '''
        # self.shop_title_label.setText("sssss")
        url=self.farm_combo.currentText()
        req=requests.get(url)
        soup=BeautifulSoup(req.text, 'html.parser')
        self.shop_title_label.setText(soup.find('title').text.strip())
        # self.init_date_combo()
        # self.tablewidget.clear()
        # self.shop_title_label.setText("aaa")

class ContactDetail(QWidget):
    def __init__(self):
        super().__init__()
        vboxmain=QVBoxLayout()
        vbox1=QVBoxLayout()
        groupbox=QGroupBox('Select gender')
        
        combo=QComboBox()
        li=['male', 'female']
        combo.addItems(li)
        vbox1.addWidget(combo)
        groupbox.setLayout(vbox1)
        
        groupbox2=QGroupBox('select your language')
        ch1=QCheckBox('C++')
        ch2=QCheckBox("java")
        ch3=QCheckBox('c#')
        vbox2=QVBoxLayout()
        vbox2.addWidget(ch1)
        vbox2.addWidget(ch2)
        vbox2.addWidget(ch3)
        
        groupbox2.setLayout(vbox2)
        
        vboxmain.addWidget(groupbox)
        vboxmain.addWidget(groupbox2)
        self.setLayout(vboxmain)

class ImageLoad(QWidget):
    def __init__(self):
        super().__init__()
        btn=QPushButton("load image")
        self.lb=QLabel("hello")
        btn.clicked.connect(self.imBtn)
        vbox=QVBoxLayout()
        vbox.addWidget(btn)
        vbox.addWidget(self.lb)
        self.setLayout(vbox)
        
    def imBtn(self):
        fname=QFileDialog.getOpenFileName(self,'파일이름?','D:\Program Files\WarCraft II\IMG\잡지부록판CD-COVER')
        imagePath=fname[0]
        pixmap=QPixmap(imagePath)
        self.lb.setPixmap(QPixmap(pixmap))
        # self.resize(pixmap.width(), pixmap.height())
    

App=QApplication(sys.argv)
win=Window()
win.show()
App.exec()
