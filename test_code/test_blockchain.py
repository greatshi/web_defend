import json
import requests
import urllib2
import urllib
import pprint


def do_post(url, data):
    data = urllib.urlencode(data)
    resp = urllib2.urlopen(url, data).read()
    return resp


def test_register_nodes():
    url = 'http://127.0.0.1:5000/nodes/register'
    nodes = {'action': 'register_nodes',
             'nodes': ['http://127.0.0.1:5001', 'http://127.0.0.1:5002']}
    print do_post(url, nodes)

    url = 'http://127.0.0.1:5001/nodes/register'
    nodes = {'action': 'register_nodes',
             'nodes': ['http://127.0.0.1:5000', 'http://127.0.0.1:5002']}
    print do_post(url, nodes)

    url = 'http://127.0.0.1:5002/nodes/register'
    nodes = {'action': 'register_nodes',
             'nodes': ['http://127.0.0.1:5000', 'http://127.0.0.1:5001']}
    print do_post(url, nodes)


def test_new_transaction():
    url = 'http://127.0.0.1:5000/transactions/new'
    transactions = {'sender': '5000', 'recipient': 'hahahahah',
                    'amount': '7'}
    print do_post(url, transactions)


def test_django_mine():
    url = 'http://127.0.0.1:8000/miner/'
    transactions = {'action': 'mine'}
    print do_post(url, transactions)


def test_django_full_chain():
    url = 'http://127.0.0.1:8000/miner/'
    action = {'action': 'full_chain'}
    data = urllib.urlencode(action)
    response = do_post(url, action)
    # print eval(response)[0]['chain']
    pprint.pprint(eval(do_post(url, action))[0]['chain'])
    # print eval(response)[0]['chain'][6]['transactions']
    # print eval(response)[0]['chain'][5]['transactions'][0]['trans_id']


# def test_django_new_transaction():
#     url = 'http://127.0.0.1:8000/miner/'
#     action = {'action': 'new_transaction', 'sender': '5000',
#               'recipient': 'hahahahah', 'amount': '7'}
#     print do_post(url, action)


def test_django_consensus():
    url = 'http://127.0.0.1:8000/miner/'
    action = {'action': 'consensus'}
    print do_post(url, action)


def main():
    # test_register_nodes()
    # test_django_new_transaction()
    # test_new_transaction()
    # test_django_mine()
    test_django_full_chain()
    # test_django_consensus()

if __name__ == '__main__':
    main()
