import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
URL="https://search.shopping.naver.com/search/all.nhn?query=데스크오거나이저&cat_id=&frm=NVSHATC"
ITEM_PER_PAGE=40

def find_global_max(words):
    # 페이지를 넘기면서 최대 검색페이지 찾기
    url=f"https://search.shopping.naver.com/search/all.nhn?query={words}&cat_id=&frm=NVSHATC"
    # print(words, "...")
    last_page=0
    while last_page < 100:
        html=requests.get(url)
        soup=BeautifulSoup(html.text, 'html.parser')
        pagination=soup.find("div", {"id":"_result_paging"})
        pages=pagination.find_all("a")
        if pages[-1].string !='다음':
            last_page=int(pages[-1].string)+1
            return last_page
        else:
            last_page=int(pages[-2].string)
            #print(f"checked {last_page}")
            url=f"https://search.shopping.naver.com/search/all.nhn?origQuery={words}&pagingIndex={last_page}&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query={words}"
    return last_page

def find_max_page(words):
    '''
    네이버쇼핑에서 검색시 뜨는 최대 페이지수 10 Page이하
    '''
    url=f"https://search.shopping.naver.com/search/all.nhn?query={words}&cat_id=&frm=NVSHATC"
    html=requests.get(url)
    soup=BeautifulSoup(html.text, 'html.parser')
    # id="_result_paging"
    pagination=soup.find("div", {"id":"_result_paging"})
    if pagination is None:
        return 0
    
    pages=pagination.find_all("a")
    if pages == []:
        return 1

    if pages[-1].string=='다음':
        return int(pages[-2].string)
    else:
        return int(pages[-1].string)

def find_item(words, mall='헤이해나'):
    ##old version. Use find_item2
    url=f"https://search.shopping.naver.com/search/all.nhn?query={words}&cat_id=&frm=NVSHATC"
    html=requests.get(url)
    soup=BeautifulSoup(html.text, 'html.parser')
    goods=soup.find("ul",{"class":"goods_list"})
    items=goods.find_all("li", {"class":"_itemSection"})
    i=1
    foundflag=False
    for item in items:
        info_mall=item.find("div",{"class":"info_mall"})
        mall_name=info_mall.find("a",{"class":"btn_detail"})['data-mall-name']
        i=i+1
        if(mall_name==mall) :
            return i
    return -1

def find_item2(keyword, mall='헤이해나'):
    '''
    keyword를 naver shopping에서 검색하였을때 
    mall에서 검색되는 페이지 도출
    Input 
        keyword
        mall
    Output
        (페이지, 순번)
    '''
    url=f"https://search.shopping.naver.com/search/all.nhn?query={keyword}&cat_id=&frm=NVSHATC"
    max_page=find_max_page(keyword)
    # max_page=min(6, max_page)
    # max_page=27
    for page in range(max_page):
        # page starts 0 which is page 1, refer it as page+1
        p=page+1
        url_p=f"https://search.shopping.naver.com/search/all.nhn?origQuery={keyword}&pagingIndex={p}&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query={keyword}"
        html=requests.get(url_p)
        soup=BeautifulSoup(html.text, 'html.parser')
        goods=soup.find("ul",{"class":"goods_list"})
        try:
            items=goods.find_all("li", {"class":"_itemSection"})
            i=1
            for item in items:
                info_mall=item.find("div",{"class":"info_mall"})
                # info=item.find("div",{"class":"info"})
                #print(i)
                try:
                    mall_name=info_mall.find("a",{"class":"btn_detail"})['data-mall-name']
                # item_name=info.find("a",{"class":"link"}).text
                except:
                    mall_name=''
                    
                if(mall_name==mall) :
                    return p,i,url_p
                i=i+1   
        except:
            return None, None, None       
        #print(f"not found in page{p}")
    return None, None,None

def find_item3(words, mall='헤이해나'):
    # 바닐라 request로는 찜이 안받아짐
    # jjim.py에서 selenium으로 받기

    url=f"https://search.shopping.naver.com/search/all.nhn?query={words}&cat_id=&frm=NVSHATC"
    max_page=find_max_page(words)
    # max_page=27
    itemslist=[]
    for page in range(max_page):
        # page starts 0 which is page 1, refer it as page+1
        p=page+1
        url_p=f"https://search.shopping.naver.com/search/all.nhn?origQuery={words}&pagingIndex={p}&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query={words}"
        html=requests.get(url_p)
        soup=BeautifulSoup(html.text, 'html.parser')
        goods=soup.find("ul",{"class":"goods_list"})
        items=goods.find_all("li", {"class":"_itemSection"})
        i=1
        for item in items:
            info_mall=item.find("div",{"class":"info_mall"})
            info=item.find("div",{"class":"info"})
            mall_name=info_mall.find("a",{"class":"btn_detail"})['data-mall-name']
            item_name=info.find("a",{"class":"link"}).text
            jjim=info.find("a",{"class":"jjim _jjim"}).text
            i=i+1
            if(mall_name==mall) :
                itemslist.append({"mall":mall_name, "item_name":item_name, "jjim":jjim[3:]})        
            
    return itemslist

def find_product_id(url_mall):
    '''
    mall의 모든 상품의 product id를 찾음
    url_mall:  https://smartstore.naver.com/heyhannah

    '''
def find_total_items_old(words):
    '''
    마지막페이지를 찾아서 검색수량 계산하는 방식, 불완전함. 
    첫페이지의 '전체 1.234'를 가져오는 방식으로 고칠것
    '''
    words=quote_plus(words, 'utf-8')
    max_p=find_global_max(words)
    url_p=f"https://search.shopping.naver.com/search/all.nhn?origQuery={words}&pagingIndex={max_p}&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query={words}"
    html=requests.get(url_p)
    soup=BeautifulSoup(html.text, 'html.parser')
    goods=soup.find("ul",{"class":"goods_list"})
    items=goods.find_all("li", {"class":"_itemSection"})
    tot_items=ITEM_PER_PAGE*(max_p-1)+len(items)
    return tot_items,f"https://search.shopping.naver.com/search/all.nhn?query={words}&cat_id=&frm=NVSHATC"

def find_total_items(words):
    '''
    첫페이지의 '전체 1.234'를 가져오는 방식
    '''
    words=quote_plus(words, 'utf-8')
    url=f'https://search.shopping.naver.com/search/all.nhn?query={words}&cat_id=&frm=NVSHATC'
    html=requests.get(url)
    soup=BeautifulSoup(html.text, 'html.parser')
    ls=soup.find("li", {'class': 'snb_all on'})
    ls.em.decompose()
    num=int((ls.text.strip()).replace(',', ''))
    return num, f"https://search.shopping.naver.com/search/all.nhn?query={words}&cat_id=&frm=NVSHATC"

if __name__=="__main__":
    # html=requests.get(URL)
    # soup=BeautifulSoup(html.text, 'html.parser')
    # goods=soup.find("ul",{"class":"goods_list"})
    # # items=soup.find("li", {"class":"-itemSection"})
    # # print(len(items))
    # items=goods.find_all("li", {"class":"_itemSection"})
    # i=1
    # foundflag=False
    # for item in items:
    #     info_mall=item.find("div",{"class":"info_mall"})
    #     mall_name=info_mall.find("a",{"class":"btn_detail"})['data-mall-name']
    #     i=i+1
    #     if(mall_name=='헤이해나') :
    #         print(f"{i}번째몰000 {mall_name}")

    # max_page=find_max_page('데스크오거나이저')
    # print(max_page)
    # page=2
    #=========================================
    words='티코스터'
    mall='헤이해나'
    p,i,u= find_item2(words, mall)
    print(p,i,u)
    #========================================
    #mp=find_max_page('핸드메이드 양모 울 동물 티코스터')
    #print(mp)
    # url=f"https://search.shopping.naver.com/search/all.nhn?origQuery={words}&pagingIndex={page}&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query={words}"
    # print(url)

    # pagenum, itemnum= find_item2(words,mall)
    # if pagenum==None:
    #     print("not found")
    # else:
    #     print(f"found {words} in {pagenum} page/{itemnum}th item")
    
    # global_page= find_global_max(words)
    # print(global_page)

    
    # tntnitems=find_item3("헤이해나")
    # i=1
    # print("total items ", len(items) )
    # print("=============")
    # for item in items:
    #     print(f"{i} 상품명 {item['item_name']} 찜 {item['jjim']}")
    #     i+=1
    # print(find_global_max('데스크오거나이저'))
    # print(find_total_items('데스크오거나이저'))

