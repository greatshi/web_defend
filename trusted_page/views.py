# coding=utf-8


from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


import json
import random
import urllib
import urllib2
import chardet
import time
import pyecc


import web_server.blockchain as blockchain
# from trusted_page.models import Transaction


# Create your views here.
def trusted_page(request):
    return render(request, 'index.html', locals())


def do_post(url, data):
    data = urllib.urlencode(data)
    resp = urllib2.urlopen(url, data).read()
    return resp


def cards_info():
    url = 'http://127.0.0.1:8000/miner/'
    action = {'action': 'full_chain'}
    num_0 = int(eval(do_post(url, action))[0]['length'])
    percentage_0 = int(num_0/100)

    url = 'http://127.0.0.1:8000/miner/'
    action = {'action': 'get_transactions'}
    num_1 = int(eval(do_post(url, action))[0]['transactions_num'])
    percentage_1 = int(num_1/0.1)

    action = {'action': 'get_nodes'}
    num_2 = int(eval(do_post(url, action))[0]['nodes_num'])
    percentage_2 = int(num_2/0.09)

    num_3 = random.randint(5700, 5790)
    percentage_3 = int(num_3/100)
    cards_info = [{"num_0": num_0, "percentage_0": percentage_0,
                   "num_1": num_1, "percentage_1": percentage_1,
                   "num_2": num_2, "percentage_2": percentage_2,
                   "num_3": num_3, "percentage_3": percentage_3}]
    return cards_info


def server_info():
    server_info =[
    {
        "name": "File Server",
        "data": [{"x": 1893456000, "y": 77}, {"x": 1893456101, "y": 87},
                 {"x": 1893456202, "y": 97}, {"x": 1893456303, "y": 57},
                 {"x": 1893456404, "y": 67}, {"x": 1893456501, "y": 87},
                 {"x": 1893456602, "y": 77},
                 {"x": 1893456703, "y": random.randint(67, 100)},
                 {"x": 1893456804, "y": 97}, {"x": 1893456901, "y": 57},
                 {"x": 1893457002, "y": random.randint(67, 100)},
                 {"x": 1893457103, "y": 67}, {"x": 1893457204, "y": 87}]
    }, {
        "name": "Mail Server",
        "data": [{"x": 1893456000, "y": 87}, {"x": 1893456101, "y": 87},
                 {"x": 1893456202, "y": 87}, {"x": 1893456303, "y": 57},
                 {"x": 1893456404, "y": random.randint(67, 100)},
                 {"x": 1893456501, "y": random.randint(67, 100)},
                 {"x": 1893456602, "y": 87}, {"x": 1893456703, "y": 67},
                 {"x": 1893456804, "y": random.randint(67, 100)},
                 {"x": 1893456901, "y": 79}, {"x": 1893457002, "y": 87},
                 {"x": 1893457103, "y": random.randint(67, 100)},
                 {"x": 1893457204, "y": random.randint(67, 100)}
                 ]
    }]
    # os.popen('df -h|grep disk3s1').read().split(' ')[14]
    return server_info


def page_diff(page_content, last_page_content):
    page_one = page_content.split('\n')
    page_another = last_page_content.split('\n')

    diff = ''
    diff += 'now add: \n' + '*'*40 + '\n'
    for i in page_one:
        if i not in page_another:
            diff += i

    diff += '\n'+'*'*40 + '\n\nbefore: \n' + '*'*40 + '\n'
    for i in page_another:
        if i not in page_one:
            diff += i
    return diff


def page_balance(page_name):
    with open('page_balance.txt', 'r') as f:
        page_balance_dict = eval(f.read())
    page_balance = 0
    for i in page_balance_dict:
        if ((i['page_name'] == page_name) and
           (int(time.time())-int(i['timestamp']) < 5)):
            page_balance += 1
    page_balance = page_balance/1.0
    if (page_balance > 100):
        page_balance = random.randint(95, 99)
    elif (page_balance == 0):
        page_balance = random.randint(5, 7)
    else:
        page_balance += random.randint(0, 1)
    return page_balance


def search_transaction_by_name(page_name):
    url_miner = 'http://127.0.0.1:8000/miner/'
    action = {'action': 'search_transaction_by_name',
              'page_name': page_name}
    return eval(do_post(url_miner, action))


def page_info(page_name, url):
    last_trans = search_transaction_by_name(page_name)
    # last_trans = Transaction.objects.filter(page_name=page_name).order_by('-timestamp')[0]

    page_content = urllib2.urlopen(url).read()
    mychar = chardet.detect(page_content)['encoding']
    page_content = page_content.decode(mychar, 'ignore').encode('utf-8')

    try:
        page_content_u = page_content.decode('utf8')
        page_content_u.split('\r\n')
    except Exception as e:
        print e
    trans_id = blockchain.compute_hash(page_content)
    diff = ''
    # if trans_id != last_trans.trans_id:
    #     diff = page_diff(page_content_u, last_trans.page_content)
    if trans_id != last_trans['trans_id']:
        diff = page_diff(page_content_u, last_trans['page_content'])

    page_balance_r = page_balance(page_name)

    # resp = {'trans_id': trans_id, 'page_name': last_trans.page_name,
    #         'last_hash': last_trans.trans_id,
    #         'timestamp': last_trans.timestamp,
    #         'diff':diff, 'page_balance':page_balance_r}
    resp = {'trans_id': trans_id, 'page_name': last_trans['page_name'],
            'last_hash': last_trans['trans_id'],
            'timestamp': last_trans['timestamp'],
            'diff': diff, 'page_balance': page_balance_r}
    return resp


def trans_resp():
    trans_resp = []

    page_name = 'web_01'
    url = 'http://127.0.0.1:8000/web_server/web_01'
    resp = page_info(page_name, url)
    trans_resp.append(resp)

    page_name = 'web_02'
    url = 'http://127.0.0.1:8000/web_server/web_02'
    resp = page_info(page_name, url)
    trans_resp.append(resp)

    # Web page web_03
    page_name = 'index.asp'
    url = 'http://int.hbu.cn/index.asp'
    resp = page_info(page_name, url)
    trans_resp.append(resp)

    # Web page web_04
    page_name = 'download'
    url = 'http://int.hbu.cn/content/?138.html'
    resp = page_info(page_name, url)

    trans_resp.append(resp)
    return trans_resp


def new_trans(url, page_name):
    sender = '10.188.14.37'
    page_content = urllib2.urlopen(url).read()
    mychar = chardet.detect(page_content)['encoding']
    page_content = page_content.decode(mychar, 'ignore').encode('utf-8')
    trans_id = blockchain.compute_hash(page_content)
    try:
        # last_trans = Transaction.objects.filter(page_name=page_name).order_by('-timestamp')[0]
        # last_hash = last_trans.trans_id
        last_trans = search_transaction_by_name(page_name)
        last_hash = last_trans['trans_id']
    except:
        last_hash = trans_id
    timestamp = str(blockchain.create_time_strap())

    # signature the transaction
    with open('keys.pem', 'r') as f:
        keys = eval(f.read())
    pub = keys[sender]['pub']
    pri = keys[sender]['pri']
    ecc = pyecc.ECC(public=pub, private=pri)
    signature = ecc.sign(trans_id)
    # signature = 'sig'
    # send to miner
    transaction = {'trans_id': trans_id, 'sender': sender,
                   'page_name': page_name, 'last_hash': last_hash,
                   'timestamp': timestamp, 'page_content': page_content,
                   'signature': signature}
    url = 'http://127.0.0.1:8000/miner/'
    action = {'action': 'new_transaction', 'transaction': transaction}
    response = do_post(url, action)
    response = eval(response)[0]['message']

    # save to database
    # trans = Transaction(trans_id=trans_id, sender=sender,
    #                     page_name=page_name,
    #                     last_hash=last_hash, timestamp=timestamp,
    #                     page_content=page_content, signature=signature)
    # trans.save()
    return response


def web_change(web_id):
    if web_id == '01':
        url = 'http://127.0.0.1:8000/web_server/web_01'
        page_name = 'web_01'
        msg = new_trans(url, page_name)

    elif web_id == '02':
        url = 'http://127.0.0.1:8000/web_server/web_02'
        page_name = 'web_02'
        msg = new_trans(url, page_name)

    elif web_id == '03':
        url = 'http://int.hbu.cn/index.asp'
        page_name = 'index.asp'
        msg = new_trans(url, page_name)

    elif web_id == '04':
        url = 'http://int.hbu.cn/content/?138.html'
        # url = 'http://127.0.0.1:8000/web_server/web_01'
        page_name = 'download'
        msg = new_trans(url, page_name)
    else:
        msg = 'None'

    change_info = [{'web_id': web_id, 'msg': msg}]
    return change_info


@csrf_exempt
def data(request):
    id = request.POST.get('id', None)

    info = server_info()
    # info = ''
    if id == 'cards':
        info = cards_info()
    elif id == 'trans':
        info = trans_resp()
    elif id == 'change':
        web_id = request.POST.get('web_id', None)
        info = web_change(web_id)
    response = HttpResponse()
    # response['Content-Type'] = "text/javascript"
    rjson = json.dumps(info)
    response.write(rjson)
    return response
