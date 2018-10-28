# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from trusted_page.models import Transaction


import time


import blockchain


def web_server(request):
    # import os
    # print os.getcwd()
    return render(request, '2ndex.html', locals())


def add_page_balance(page_name):
    try:
        with open('page_balance.txt', 'r') as f:
            page_balance = eval(f.read())
    except:
        page_balance = []
    page_balance.append({'page_name': page_name,
                        'timestamp': str(int(time.time()))})
    with open('page_balance.txt', 'w+') as f:
        f.write(str(page_balance))


def web_01(request):
    page_name = 'web_01'
    add_page_balance(page_name)
    with open('web_server/templates/2ndex.html', 'rb') as f:
        page_content = f.read()
    trans_id = blockchain.compute_hash(page_content)
    try:
        last_trans = Transaction.objects.filter(page_name=page_name).order_by('-timestamp')[0]
        last_hash = last_trans.trans_id
    except:
        last_hash = trans_id
    # timestamp = str(blockchain.create_time_strap())
    # trans = Transaction(trans_id=trans_id, page_name=page_name,
    #                     last_hash=last_hash, timestamp=timestamp)
    # trans.save()

    # if blockchain.page_test(page_content):
    if trans_id == last_hash:
        return render(request, '2ndex.html', locals())
    else:
        return render(request, '2ndex.html', locals())
        # return render(request, 'err.html', locals())


def web_02(request):
    page_name = 'web_02'
    add_page_balance(page_name)
    with open('web_server/templates/reg.html', 'rb') as f:
        page_content = f.read()
    trans_id = blockchain.compute_hash(page_content)
    try:
        last_trans = Transaction.objects.filter(page_name=page_name).order_by('-timestamp')[0]
        last_hash = last_trans.trans_id
    except:
        last_hash = trans_id
    # timestamp = str(blockchain.create_time_strap())
    # trans = Transaction(trans_id=trans_id, page_name=page_name,
    #                     last_hash=last_hash, timestamp=timestamp)
    # trans.save()

    # if blockchain.page_test(page_content):
    if trans_id == last_hash:
        return render(request, 'reg.html', locals())
    else:
        return render(request, 'reg.html', locals())
        # return render(request, 'err.html', locals())
