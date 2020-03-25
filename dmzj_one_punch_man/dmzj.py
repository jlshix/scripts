import os
from time import sleep
from pprint import pprint
from collections import deque

import execjs
from bs4 import BeautifulSoup
import requests

max_retry = 5
# get with a timeout tuple of connection and read
timeout = (5, 5)
domain = "https://manhua.dmzj.com/"
headers = {
    "Referer": domain,
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.98 Chrome/71.0.3578.98 Safari/537.36"
}

def ht_get(link, headers=headers):
    '''requests.get with retry
    returns the result of requests.get or exit with code -1
    '''
    left = max_retry
    while left:
        try:
            print('GET {}/{}: {}...'.format(max_retry-left+1, max_retry, link))
            resp = requests.get(link, headers=headers, timeout=timeout)
            if resp.ok:
                return resp
        except Exception as e:
            if left == 1:
                print(e)
        finally:
            left -= 1
    print('exit with code -1: http err occurred')
    exit(-1)
    
def get_category(link) -> list:
    '''returns a list of tuple like [(title1, link1), (title2, link2), ...]
    by analysing html of given link
    '''
    resp = ht_get(link)
    soup = BeautifulSoup(resp.text, 'lxml')
    res = []

    for div in soup.find_all('div', class_='cartoon_online_border'):
        for li in div.ul:
            if type(li).__name__ == 'Tag':
                res.append((li.a.text, domain + li.a['href']))
    
    for div in soup.find_all('div', class_='cartoon_online_border_other'):
        for li in div.ul:
            if type(li).__name__ == 'Tag':
                res.append((li.a.text, domain + li.a['href']))

    return res


def get_pic_urls(refer, link) -> list:
    '''get html from link, 
    execute js code in script block to get pic_urls
    '''
    headers['Refer'] = refer
    resp = ht_get(link, headers=headers)
    soup = BeautifulSoup(resp.text, 'lxml')

    # extract and run js code in script block
    code = 'function(){' + soup.script.text + ' return arr_pages; }()'
    head = 'https://images.dmzj.com/'
    return [head + x for x in execjs.eval(code)]


def download_pic(refer, link, folder):
    '''download pic into folder by link with refer
    '''
    print('downloading {}...'.format(link))
    headers['Refer'] = refer
    res = requests.get(link, headers=headers, timeout=timeout)

    path = os.path.join(folder, link.split('/')[-1])
    with open(path, 'wb') as f:
        f.write(res.content)

def errlog(s):
    with open('err.log', 'a+') as f:
        f.write(s+'\n')


def main(url):
    # get dir name to create folder
    title = os.path.split(url)[-1]
    if not os.path.exists(title):
        os.makedirs(title)
    
    # get category like [(title1, link1), (title2, link2), ...]
    category = get_category(url)
    # counter for sub directory
    chapter, count = 1, len(category)

    for name, link in category:
        print('processing {}/{}: {}...'.format(chapter, count, name))
        folder = '{:03}_{}'.format(chapter, name)
        path = os.path.join(title, folder)
        
        # check if it is already here
        if os.path.exists(path):
            print('{} already exists, skip to next chapter'.format(path))
            chapter += 1
            continue
        else:
            os.makedirs(path)
        
        pics = get_pic_urls(url, link)
        length = len(pics)
        queue = deque()
        # download pic one by one
        for i, pic in enumerate(pics, start=1):
            print('{:03}/{:03}, downloading {}...'.format(i, length, pic))
            try:
                download_pic(link, pic, path)
            except Exception as e:
                print('failed, added to queue')
                queue.appendleft((link, pic, path, 1))

        while queue:
            try:
                link, pic, path, times = queue.pop()
                print('at queue: retry {}/{} downloading {} to {}...'.format(times, max_retry, pic.split('/')[-1], path))
                sleep(times)
                download_pic(link, pic, path)
                print('at queue: success')
            except Exception as e:
                times += 1
                if times <= max_retry:
                    queue.appendleft((link, pic, path, times))
                    print('at queue: appendleft')
                else:
                    errlog(','.join((link, pic, path, str(e))))
                    print('at queue: failed to download {} to {},  at queue with max_retry: {}, err recorderd at err.log'
                            .format(pic.split('/')[-1], path, max_retry))
        
        chapter += 1
        print()

if __name__ == "__main__":
    main("https://manhua.dmzj.com/yiquanchaoren")
