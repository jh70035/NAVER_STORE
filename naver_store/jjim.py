from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
from urllib.parse import quote_plus
from navershopping import find_global_max
import csv
import pickle
import time

# driver=webdriver.Chrome()
# url=f'https://search.shopping.naver.com/search/all.nhn?query=헤이해나'

# html=requests.get(url)
# soup=BeautifulSoup(html.text, 'html.parser')
# items=soup.select('._itemSection')

# driver.get(url)
# html=driver.page_source
# soup=BeautifulSoup(html, 'html.parser')
# items=soup.select('._itemSection')

# for item in items:
#     item_name=item.find("div", {"class":"info"}).find("div", {"class":"tit"}).find("a").text
#     jjim=item.find("a", {"class":"jjim _jjim"}).text
#     review=item.find('a', {'class':'graph'}).text
#     print(review[2:])
#     print(item_name, jjim[3:])
#     break


def all_items(mall_name='헤이해나'):
    '''
    네이버 쇼핑에서 몰이름으로 검색했을때 보이는 아이템으로 찾기
    모든 상품의 검색되지 않는 문제
    OUTPUT : {"name":item_name, "mall":mall_name, "jjim":jjim, 'review':review, 'sold':sold, 'pid':pid}
    '''
    url=f"https://search.shopping.naver.com/search/all.nhn?query={mall_name}"
    # url2=f"https://search.shopping.naver.com/search/all.nhn?origQuery={mall_name}&pagingIndex=2&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query={mall_name}"
    # max_page=find_global_max(mall_name)
    max_page=4
    driver=webdriver.Chrome()

    itemslist=[]
    for p in range(max_page):
        if p>0:
            url=f"https://search.shopping.naver.com/search/all.nhn?origQuery={mall_name}&pagingIndex={p+1}&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query={mall_name}"
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        items=soup.select("._itemSection")

        for item in items:
            info_mall=item.find("div", {"class":"info_mall"})
            # name_detail= info_mall.find("a", {"class":"btn_detail _btn_mall_detail"})['data-mall-name']
            mallname= info_mall.find("a", {"class":"btn_detail _btn_mall_detail"})['data-mall-name']    
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
       
                itemslist.append({"name":item_name, "mall":mall_name, "jjim":jjim, 'review':review, 'sold':sold, 'pid':pid})
    return itemslist


def all_items2(url_mall='https://smartstore.naver.com/heyhannah'):
    '''
    쇼핑몰 홈에서 직접 전체 상품 찾기
    under construction...
    '''
    # url=f"https://search.shopping.naver.com/search/all.nhn?query={mall_name}"
    # url2=f"https://search.shopping.naver.com/search/all.nhn?origQuery={mall_name}&pagingIndex=2&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query={mall_name}"
    # max_page=find_global_max(mall_name)
    url_mall_all=url_mall+'/category/ALL?cp=1'
    driver=webdriver.Chrome()


    itemslist=[]
    for p in range(max_page):
        if p>0:
            url=f"https://search.shopping.naver.com/search/all.nhn?origQuery={mall_name}&pagingIndex={p+1}&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query={mall_name}"
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        items=soup.select("._itemSection")

        for item in items:
            info_mall=item.find("div", {"class":"info_mall"})
            # name_detail= info_mall.find("a", {"class":"btn_detail _btn_mall_detail"})['data-mall-name']
            mallname= info_mall.find("a", {"class":"btn_detail _btn_mall_detail"})['data-mall-name']    
            # print(name_detail)
            
            if mallname==mall_name:
                item_name=item.find("div", {"class":"info"}).find("div", {"class":"tit"}).find("a").text
                #print(item_name)
                jjim=''
                review=''
                sold=''
                jjim=item.find("a", {"class":"jjim _jjim"}).text
                jjim=jjim[3:]
                etc=item.find('div', {'class':'info'}).find('span', {'class':'etc'}).find_all('a')
                for a_tag in etc:
                    # print(a_tag.text[:2])
                    if a_tag.text[:2]=="리뷰":
                        review=a_tag.text[2:]
                    if a_tag.text[:2]=="구매":
                        sold=a_tag.text[4:]
       
                itemslist.append({"name":item_name, "mall":mall_name, "jjim":jjim, 'review':review, 'sold':sold})
    return itemslist

def save(result):
    import time
    now=time.localtime()
    fname=f"./csv/heyhanna{now.tm_mon}{now.tm_mday}{now.tm_hour}{now.tm_min}.csv"
    file=open(fname, "w", newline='', encoding='utf-8')
    writer=csv.writer(file)
    writer.writerow(["상품명", "리뷰",'구매하기' ,"찜", 'ID' ])

    for item in result:
        writer.writerow([item['name'], item['review'],item['sold'],item['jjim'],item['pid']])
    file.close()



if __name__=="__main__":


    # itemslist=all_items('헤이해나')
    # with open('itemslist.pickle','wb') as f:
    #     pickle.dump(itemslist, f)
    # with open('itemslist.pickle','rb') as f:
    #     itemslist=pickle.load(f)
    
    
    i=0
    for item in itemslist[:]:
        print(i,item['name'])
        baseUrl="https://smartstore.naver.com/heyhannah/products/"
        result=requests.get(f"{baseUrl}{item['pid']}")

        soup=BeautifulSoup(result.text, 'html.parser')
        try:
            tags=soup.find("div", {"class":"goods_tag"}).find_all("li")
        except:
            tags=[]
            
        taglist=[]
        for tag in tags:
            tag_str=tag.find("a").text
            taglist.append(tag_str[1:])

        item['taglist']=[item['name']]+taglist 
        i+=1
        
        #break #-----------------------
        # if i==2:
        #     break

    now=time.localtime()
    fname=f"./csv/heyhanna{now.tm_mon}{now.tm_mday}{now.tm_hour}{now.tm_min}.csv"
    file=open(fname, "w", newline='', encoding='utf-8')
    writer=csv.writer(file)    

    for item in itemslist[:]:
        # for tag in item['taglist']+item['name']:
        print(item['name'])
        writer.writerow([item['name'],'키워드', '검색페이지', '페이지내 순번', '링크'])
        
        for tag in item['taglist']:
            print(tag)
            p,i,url=find_item2(tag,'헤이해나')
            writer.writerow([tag, p, i ,url])
            print(tag,p,i)
    file.close()







    #print(itemslist[0])
    #save(itemslist)
    # print(itemslist)
    
    # print(f"총 상품수:{len(itemslist)}\n=================")
    # i=1
    # for item in itemslist:
    #     print(f"{i} 상품명:{item['name']} 찜:{item['jjim']}")
    #     i+=1

# print(len(items))

# html=urlopen(url)
# soup=BeautifulSoup(html, 'html.parser')
# # print(soup)
# items=soup.find("li", {"class": "_itemSection"})
# # info_mall=items.find("div", {"class":"info_mall"})
# print(info_mall)
# name_detail= info_mall.find("a", {"class":"btn_detail _btn_mall_detail"})['data-mall-name']

# print(name_detail)
# print(info_mall)

# n=items[0].find("div", {"class":"info_mall"}).find("a", {"class":"btn_detail _btn_mall_detail"})['data-mall-name']
# items=soup.find_all("li", {"class": "_itemSection"})
# print(len(items))
# print(len(items))

# for item in items:
#     print(item)
#     break
    # print(item.find("div", {"class":"info_mall"})).find("a", {"class":"btn_detail _btn_mall_detail"})
    # info_mall=item.find("div", {"class":"info_mall"})

#   https://search.shopping.naver.com/search/all.nhn?query=%ED%97%A4%EC%9D%B4%ED%95%B4%EB%82%98
# https://search.shopping.naver.com/search/all.nhn?origQuery=%ED%97%A4%EC%9D%B4%ED%95%B4%EB%82%98&pagingIndex=2&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query=%ED%97%A4%EC%9D%B4%ED%95%B4%EB%82%98