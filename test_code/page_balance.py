import urllib2
import time


def do_get(url):
    resp = urllib2.urlopen(url)
    return resp


def main():
    url = 'http://10.188.14.207:8000/web_server/web_02'
    for i in range(0, 1000):
        do_get(url)
        time.sleep(0.05)


if __name__ == '__main__':
    main()
