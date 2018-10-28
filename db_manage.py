#coding=utf-8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_defend.settings")

import django
django.setup()

from trusted_page.models import Transaction
import web_server.blockchain as blockchain

from django.core.serializers import serialize


def insert_db():
    with open('web_server/templates/2ndex.html', 'rb') as f:
        page_content = f.read()
    trans_id = blockchain.compute_hash(page_content)
    page_name = 'web_server/templates/2ndex.html'
    last_hash = blockchain.compute_hash(page_content)
    timestamp = str(blockchain.create_time_strap())
    trans = Transaction(trans_id=trans_id, page_name=page_name, last_hash=last_hash, timestamp=timestamp)
    trans.save()
    return 'ok'

def get_some():
    # trans = Transaction.objects.values_list('trans_id', 'page_name', 'last_hash', 'page_content', 'timestamp')
    # print trans[20]
    page_name = 'index.asp'
    last_trans = Transaction.objects.filter(page_name=page_name).order_by('-timestamp')[0]
    page_content = last_trans.page_content
    # if '\r\n' in page_content:
    #     print page_content.split('\r\n')
    # else:
    #     print page_content.split('\n')
    print page_content.split('\n')

def get_last():
    # last_trans = Transaction.objects.all().reverse()[0]
    page_name = 'index.asp'
    last_trans = Transaction.objects.filter(page_name=page_name).order_by('-timestamp')[0]
    last_trans2 = Transaction.objects.filter(page_name=page_name).order_by('-timestamp')[1]
    print last_trans.timestamp
    print last_trans.last_hash
    print last_trans2.timestamp
    print last_trans2.last_hash

def fetch_some():
    some = Transaction.objects.all()[:10]
    # print some[0].__dict__
    null = ''
    print eval(serialize('json', Transaction.objects.all()[:2]))[1]['fields']['page_name']
    print len(eval(serialize('json', Transaction.objects.all()[:5])))
    # print some[7].page_content
    # print type(some[7].page_content)

def delete_data():
    Transaction.objects.all().delete()

def main():
    # get_some()
    fetch_some()
    print '-----' * 20
    # get_last()
    # print delete_data()
    # print insert_db()

if __name__ == '__main__':
    main()
