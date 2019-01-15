import os
from pprint import pprint

import execjs
from bs4 import BeautifulSoup
import requests

domain = "https://manhua.dmzj.com/"
headers = {
    "Referer": domain,
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.98 Chrome/71.0.3578.98 Safari/537.36"
}

def get_category(link) -> list:
    '''returns a list of tuple like [(title1, link1), (title2, link2), ...]
    by analysing html of given link
    '''
    req = requests.get(link, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    res = []

    for div in soup.find_all('div', class_='cartoon_online_border'):
        for li in div.ul:
            if type(li).__name__ == 'Tag':
                res.append((li.a['title'], domain + li.a['href']))
    
    for div in soup.find_all('div', class_='cartoon_online_border_other'):
        for li in div.ul:
            if type(li).__name__ == 'Tag':
                res.append((li.a['title'], domain + li.a['href']))

    return res


def get_pic_urls(refer, link) -> list:
    '''get html from link, 
    execute js code in script block to get pic_urls
    '''
    headers['Refer'] = refer
    req = requests.get(link, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')

    # extract and run js code in script block
    code = 'function(){' + soup.script.text + ' return arr_pages; }()'
    head = 'https://images.dmzj.com/'
    return [head + x for x in execjs.eval(code)]


def download_pic(refer, link, folder):
    '''download pic by link with refer
    '''
    print('downloading {}...'.format(link))
    headers['Refer'] = refer
    res = requests.get(link, headers=headers)

    path = os.path.join(folder, link.split('/')[-1])
    with open(path, 'wb') as f:
        f.write(res.content)


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
        folder = '{:03}_{}'.format(chapter, name.split('-')[-1])
        path = os.path.join(title, folder)
        
        # check if it is already here
        if os.path.exists(path):
            print('{} already exists, skip to next chapter'.format(path))
            chapter += 1
            continue
        else:
            os.makedirs(path)
        
        # download pic one by one
        for pic in get_pic_urls(url, link):
            download_pic(link, pic, path)
        chapter += 1
        print()

if __name__ == "__main__":
    main("https://manhua.dmzj.com/yiquanchaoren")
        