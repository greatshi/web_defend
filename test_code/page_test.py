#!/usr/bin/env python
# coding=utf-8


import urllib2
import chardet


def craw_page(url):
    page_content = urllib2.urlopen(url).read()
    mychar = chardet.detect(page_content)['encoding']
    page_content = page_content.decode(mychar, 'ignore').encode('utf-8')
    print page_content.split('\r\n')

    with open('index.asp', 'w') as f:
        f.write(page_content)


def page_diff():
    with open('index.asp', 'r') as f:
        page_one = f.readlines()
    with open('2ndex.asp', 'r') as f:
        page_another = f.readlines()
    changed = 0
    diff = ''
    diff += 'f1 have: \n' + '*'*20 + '\n'
    for i in page_one:
        if i not in page_another:
            diff += i
            changed = 1

    diff += 'f2 have: \n' + '*'*20 + '\n'
    for i in page_another:
        if i not in page_one:
            diff += i
            changed = 1
    print diff


def main():
    url = 'http://int.hbu.cn/index.asp'
    # url = 'http://127.0.0.1:8000/web_server/web_01'
    craw_page(url)
    # page_diff(url)


if __name__ == '__main__':
    main()
