import requests
from bs4 import BeautifulSoup
import random
import re
import os
import hashlib
import time
import threading
from multiprocessing import Pool #进程池

STORAGE_DIR = r'C:\STORAGE\fengniao'
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
]

START_URL = 'http://image.fengniao.com/index.php?action=getList&class_id=192&sub_classid=0&page={}&not_in_id=5357901,5357786,5357739'

def get_content(url):
    '''
    返回url的html内容
    :param url:
    :return:
    '''
    headers = {
        'User-Agent':random.choice(USER_AGENT_LIST),
        'Cookie':'ip_ck=4cGG4v7xj7QuNjY3NTQ2LjE1NjY4MjkzNTA%3D; lv=1566829353; vn=1; Adshow=1; Hm_lvt_916ddc034db3aa7261c5d56a3001e7c5=1566829355; Hm_lpvt_916ddc034db3aa7261c5d56a3001e7c5=1566830725',
    }
    r = requests.get(url,headers=headers,timeout=2)
    if r.status_code == 200:
        return r.text

def list_page_parse(content):
    '''
    列表页解析，获取详情页
    :param content:
    :return:
    '''
    urls = re.findall('"pic_url":"(.*?)",',content)
    new_urls = []
    for url in urls:
        url = url.replace('\\','')
        new_urls.append(url)
    return new_urls


def download_picture(urls):
    '''
    根据url，下载图片，保存到指定位置
    :param url:
    :return:
    '''
    headers = {
        'User-Agent':random.choice(USER_AGENT_LIST),
        'Cookie':'ip_ck=4cGG4v7xj7QuNjY3NTQ2LjE1NjY4MjkzNTA%3D; lv=1566829353; vn=1; Adshow=1; Hm_lvt_916ddc034db3aa7261c5d56a3001e7c5=1566829355; Hm_lpvt_916ddc034db3aa7261c5d56a3001e7c5=1566830725',
    }
    for url in urls:
        try:
            r = requests.get(url,headers=headers,timeout=3)
        except:
            continue
        filepath = os.path.join(STORAGE_DIR,get_md5(url)+'.jpg')
        print(filepath)
        time.sleep(random.randint(1,4))
        if r.status_code == 200 and not os.path.exists(filepath):
            f = open(filepath,'wb')
            f.write(r.content)
            f.close()
            print('{} download success'.format(filepath))


def get_md5(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()



def fengniao(num):
    content = get_content(START_URL.format(num))
    print(threading.current_thread().getName())
    return list_page_parse(content)


if __name__ == '__main__':
    n = os.cpu_count()

    p = Pool(n)
    task_list = []
    for i in range(100,130):
        task = p.apply_async(fengniao,args=(i,),callback=download_picture)
        task_list.append(task)
    p.close()
    p.join()
    for task in task_list:
        print(task.get())


