# coding: utf-8
# created by jlshix on 2020-03-23

"""从风之动漫下载海贼王漫画
"""

import re
import requests
from PIL import Image
from io import BytesIO
import os
from random import random
from time import sleep
from faker import Faker

fake = Faker()
page_url = "https://manhua.fzdm.com/02//{ep}/index_{i}.html"
pic_url = "http://www-mipengine-org.mipcdn.com/i/p2.manhuapan.com/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}


def random_headers():
    """随机 headers"""
    return {'User-Agent': fake.user_agent()}


def save_pic(url, name):
    """根据 url 下载图片, 并存储为 name"""
    resp = requests.get(url)
    img = Image.open(BytesIO(resp.content))
    img = img.convert('RGB')
    img.save(name)


def get_single(ep, i, retry=5):
    """根据话数 ep 和页数 i (从 0 开始) 获取单个网页的图片, 连接不上时重试
    返回元组, 第一个为是否最后一张, 第二个为图片url"""
    if retry == 0:
        raise Exception(f"ERROR: 下载第 {i + 1} 张时出现错误")
    url = page_url.format(ep=ep, i=i)
    resp = requests.get(url, headers=random_headers())
    print(f"{resp.status_code}: {url}")
    if resp.status_code != 200:
        sleep(random() + 3)
        print(f'WARNING: 获取第{i + 1}张失败, 等待5s后重试...')
        return get_single(ep, i, retry=retry-1)

    return '最后一页了' in resp.text, pic_url + re.findall(r'var mhurl="(.*?)"', resp.text)[0]


def get_episode(ep):
    """获取某一话"""
    if isinstance(ep, int):
        ep = str(ep)
    if not os.path.exists(ep):
        os.mkdir(ep)

    i = 0
    is_last, pic = get_single(ep=ep, i=i)
    save_pic(url=pic, name=f"{ep}/{i + 1:02}.jpg")

    while not is_last:
        sleep(random() + 1)
        i += 1
        is_last, pic = get_single(ep=ep, i=i)
        save_pic(url=pic, name=f"{ep}/{i + 1:02}.jpg")
    print(f"第 {ep} 话下载完成, 共计 {i + 1} 张")


if __name__ == '__main__':
    for ep in range(931, 976):
        get_episode(ep)
