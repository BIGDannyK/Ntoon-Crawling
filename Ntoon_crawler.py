import json
from selenium import webdriver
from bs4 import BeautifulSoup
from tqdm import tqdm
from multiprocessing import Process, Queue
from tqdm import tqdm

def artist(s : str):
    s = s.replace(" ", "")
    s = s.replace(",","/")
    return list(set(s.split('/')))

def genre(s : str):
    s = s.replace(" ", "")
    return s.split(',')

def tid(s: str):
    i = s.find('titleId=')
    return (s[i+8:len(s)])

if __name__ == '__main__' :
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("lang=ko_KR") 
    options.add_argument('log-level=3')
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    driver.implicitly_wait(1)
    tset = {'leggo'}
    key = 'https://comic.naver.com/webtoon/period.nhn?'
    ind = 2017
    thelist = []
    while ind <2022:
        driver.get(key+'period='+str(ind))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        fp = 'https://comic.naver.com'
        webtoon_list = soup.select('#content > div.list_area.daily_img > ul > li > dl > dt > a')
        toondict = {}
        for webtoon in tqdm(webtoon_list) :
            ll = len(tset)
            tset.add(webtoon['title'])
            if(len(tset)>ll):
                driver.get(fp+webtoon['href'])
                soup2 = BeautifulSoup(driver.page_source,'html.parser')
                wrt = soup2.select_one('#content > div.comicinfo > div.detail > h2 > span.wrt_nm').text.strip()
                wrt2 = soup2.select_one('#content > div.comicinfo > div.detail > p.detail_info > span.genre').text.strip()
                toondict = {'Title': webtoon['title'],
                'Artist': artist(wrt),'Genre': genre(wrt2),'Title ID': tid(webtoon['href'])}
                thelist.append(toondict)
                ll = len(tset)
        ind+=1
        
    json_dump = json.dumps(thelist,ensure_ascii=False)
    f = open('output.json','w',encoding='utf-8')
    f.write(json_dump)
    
    driver.close()