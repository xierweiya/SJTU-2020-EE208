# SJTU EE208

import os
import re
import string
import sys
import urllib.error
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup


def valid_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s


def get_page(page):
    try:
        content = urllib.request.urlopen(page, timeout=10).read()
    except urllib.error.URLError:
        return None
    else:
        return content


def get_all_links(content, page):
    links = []
    soup = BeautifulSoup(content, 'lxml')
    for i in soup.findAll('a',{'href':re.compile('^http|^/')}):
        xiangdui = i['href']
        juedui = urllib.parse.urljoin(page,xiangdui)
        links.append(juedui)
    return links


def union_dfs(a, b):
    for e in b:
        if e not in a:
            a.append(e)


def add_page_to_folder(page, content):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index.txt'  # index.txt中每行是'网址 对应的文件名'
    folder = 'html'  # 存放网页的文件夹
    filename = valid_filename(page)  # 将网址变成合法的文件名
    index = open(index_filename, 'a')
    index.write(page + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(str(content))  # 将网页存入文件
    f.close()


def crawl(seed, max_page):
    tocrawl = [seed]
    crawled = []
    count = 0

    while tocrawl and count < max_page:
        page = tocrawl.pop()
        if page not in crawled:
            print(page)
            content = get_page(page)
            if content != None:
                add_page_to_folder(page, content)
                outlinks = get_all_links(content, page)
                union_dfs(tocrawl, outlinks)
            crawled.append(page)
            count = count + 1
            print(count)
    return crawled


seed = "http://www.github.com"
max_page = 20

crawled = crawl(seed, max_page)