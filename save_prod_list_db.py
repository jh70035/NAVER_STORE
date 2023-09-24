
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite3
from datetime import datetime, timedelta

def find_global_max(words):
    # 페이지를 넘기면서 최대 검색페이지 찾기
    url=f"https://search.shopping.naver.com/search/all.nhn?query={words}&cat_id=&frm=NVSHATC"
    # print(words, "...")
    last_page=0
    while last_page < 10:
        html=requests.get(url)
        soup=BeautifulSoup(html.text, 'html.parser')
        # pagination=soup.find("div", {"id":"_result_paging"})
        pagination = soup.find("div", {"class": "pagination_pagination__6AcG4"})
        pages=pagination.find_all("a")

        if pages[-1].string !='다음':
            last_page=int(pages[-1].string)+1
            return last_page
        else:
            last_page=int(pages[-2].string)
            #print(f"checked {last_page}")
            url=f"https://search.shopping.naver.com/search/all.nhn?origQuery={words}&pagingIndex={last_page}&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query={words}"
    return last_page

def all_items(mall_name, url_home):
    '''
    네이버 쇼핑에서 몰이름으로 검색했을때 보이는 아이템으로 찾기
    모든 상품의 검색되지 않는 문제
    OUTPUT : {"name":item_name, "mall":mall_name, "jjim":jjim, 'review':review, 'sold':sold, 'pid':pid}
    '''
    url=f"https://search.shopping.naver.com/search/all.nhn?query={mall_name}"
    # url_home="https://smartstore.naver.com/heyhannah"
    # url2=f"https://search.shopping.naver.com/search/all.nhn?origQuery={mall_name}&pagingIndex=2&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query={mall_name}"
    max_page=find_global_max(mall_name)
    driver=webdriver.Chrome()

    itemslist=[]
    for p in range(max_page):
        if p>0:
            url=f"https://search.shopping.naver.com/search/all.nhn?origQuery={mall_name}&pagingIndex={p+1}&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query={mall_name}"
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        # items=soup.select("._itemSection")

        #쇼핑몰이름이 일치하는지 확인
        items = soup.find_all("div", {"class": "basicList_inner__eY_mq"})
        for item in items:
            info_mall=item.find("div", {"class":"basicList_mall_title__3MWFY"})
            # name_detail= info_mall.find("a", {"class":"btn_detail _btn_mall_detail"})['data-mall-name']
            mallname= info_mall.find("a", {"class":"basicList_mall__sbVax"}).string
            # print(name_detail)
            
            if mallname==mall_name:
                item_name=item.find("div", {"class":"info"}).find("div", {"class":"tit"}).find("a").text
                #print(item_name)
                jjim=''
                review=''
                sold=''
                jjim=item.find("a", {"class":"jjim _jjim"}).text
                jjim=jjim[3:]
                pid=''
                pid=item['data-mall-pid']
                etc=item.find('div', {'class':'info'}).find('span', {'class':'etc'}).find_all('a')
                for a_tag in etc:
                    # print(a_tag.text[:2])
                    if a_tag.text[:2]=="리뷰":
                        review=a_tag.text[2:]
                    if a_tag.text[:2]=="구매":
                        sold=a_tag.text[4:]
                if sold=='' : sold=0
                if review=='':review =0
                link=url_home+"/products/" +pid
                itemslist.append({"name":item_name, "mall":mall_name, "jjim":jjim, 'review':review, 'sold':sold, 'pid':pid,'link':link})
                # itemslist.append({"name":item_name, "mall":mall_name, "jjim":jjim, 'review':review, 'sold':sold, 'pid':pid, 'link':''})
                
    return itemslist

if __name__=="__main__":
    itemslist=all_items('몬스토리', 'https://smartstore.naver.com/monsclub')
    # print(itemslist)
    conn=sqlite3.connect('emaildb.sqlite')
    cur=conn.cursor()
    tod=datetime.today()+timedelta(days=-5)
    tod=tod.strftime('%Y-%m-%d')
    

    print(tod)
    for item in itemslist:
        # print(item['name'])
        sql=f"REPLACE INTO PROD3 (dt,title, pid,jjim, sold,review,link) VALUES('{tod}','{item['name']}','{item['pid']}','{item['jjim']}','{item['sold']}','{item['review']}','{item['link']}')"
        # print(sql)
        cur.execute(sql)
        # cur.execute('''
        #         REPLACE INTO PROD3 (dt,title, pid,jjim, sold,review,link) VALUES (?,?,?,?,?,?,?);''', (tod,item['name'],item['pid'],item['jjim'],item['sold'],item['review']))
        conn.commit()
    conn.commit()
    cur.close()