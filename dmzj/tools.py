import os
import json
from pprint import pprint
from shutil import move

from dmzj import download_pic, get_category, get_pic_urls

def download_from_log():
    '''read from err.log which is generated by dmzj.py when a pic cannot be downloaded,
    then get a list of params to re-download
    '''
    with open('err.log') as f:
        for line in (x for x in f.readlines() if x != '\n'):
            refer, link, folder = line.split(',')[:3]
            print('downloading {} to {}...'.format(link, folder))
            download_pic(refer, link, folder)


def check_local(root: str) -> list:
    '''returns a list of (folder_name, file_count) in root
    you can get the final page count by `sum(x[1] for x in res)`
    '''
    res = []
    for chapter in os.listdir(root):
        item = os.path.join(root, chapter)
        if os.path.isdir(item):
            count = sum(1 for name in os.listdir(item))
            res.append((chapter, count))
    print('page count: {}'.format(sum(x[1] for x in res)))
    return res


def check_website(url) -> list:
    '''check page count of given url of comic main page.
    since it's unpredictable in GET, write to file once get a page count result of a chapter.
    '''
    filename = 'website_res.csv'
    # read from csv file
    if os.path.exists(filename):
        with open(filename) as f:
            res = [x.strip('\n').split(',') for x in f.readlines() if x != '\n']
    else:
        with open(filename, 'w') as f:
            f.write('')
        res = []

    category = get_category(url)
    chapter, count = 1, len(category)

    # lines to skip
    saved = len(res)
    for name, link in category:
        if saved:
            saved -= 1
            continue

        print('processing {}/{}: {}...'.format(chapter, count, name))
        folder = '{:03}_{}'.format(chapter, name)
        length = len(get_pic_urls(url, link))
        tmp = (folder, length)

        # save to csv file
        with open(filename, 'a+') as f:
            f.write(','.join(str(x) for x in tmp) + '\n')
        res.append(tmp)

        chapter += 1
        print()
    
    return res


def check_integrity(root, url) -> set:
    '''compare local page count of chapters with it of website,
    returns a set of differences
    '''
    local_res = check_local(root)
    website_res = check_website(url)
    # local_res may not be in order because of the storage strategy of os
    local_res = sorted(local_res)
    # may not be necessary
    website_res = sorted(website_res)
    pprint(local_res)
    pprint(website_res)
    return set(website_res) - set(local_res)


def mktestdir(dirname, amount):
    '''generate test root directory for renamer
    '''
    if os.path.exists(dirname):
        os.remove(dirname)
    os.mkdir(dirname)
    for i in range(1, amount+1):
        os.mkdir(os.path.join(dirname, '{:03}_{:03}'.format(i, i)))


def renamer(root, dst, old_start, old_end, new_start=1):
    '''in given root directory whose structure like generated by mktestdir(dirname, amount), 
    move given range(old_start, old_end+1) at root
    to range(new_start, old_end-old_start+1) to dst
    >>> from tools import mktestdir, renamer
    >>> root = 'comic'
    >>> mktestdir(root, 200)
    >>> renamer(root, 'one', 42, 100)
    >>> renamer(root, 'two', 105, 200, 42)
    '''
    if not os.path.exists(dst):
        os.mkdir(dst)
    
    nums = [format(i, '>03') for i in range(old_start, old_end+1)]
    for d in sorted(os.listdir(root)):
        head, tail = d.split('_')
        if head in nums:
            new_head = format(nums.index(head)+new_start, '>03')
            name = '_'.join((new_head, tail))
            move(os.path.join(root, d), os.path.join(dst, name))


if __name__ == "__main__":
    root = 'yiquanchaoren'
    url = 'https://manhua.dmzj.com/yiquanchaoren'
    # download_from_log()
    # res = check_local(root)
    res = check_website(url)
    # res = check_integrity(root, url)
    pprint(res)
