# coding=utf-8


from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


import json
import random
import socket
import time
import pyecc
import copy
import hashlib
import urllib
import urllib2
import requests
from threading import Thread
from urlparse import urlparse
from uuid import uuid4


class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        try:
            with open('blockchain.txt', 'r') as f:
                self.chain = eval(f.read())
        except:
            # Create the genesis block
            self.new_block(previous_hash='1', proof=100, last_proof=9)

    def register_node(self, address):
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while (current_index < len(chain)):
            block = chain[current_index]
            if (block['previous_hash'] != self.hash(last_block)):
                return False

            if (not (self.valid_proof(last_block['proof'],
                     block['proof'], block['previous_hash']))):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for node in neighbours:
            try:
                url = 'http://'+node+'/miner/'
                data = {'action': 'full_chain'}
                data = urllib.urlencode(data)
                response = urllib2.urlopen(url, data)
                if response.getcode() == 200:
                    response = response.read()
                    length = eval(response)[0]['length']
                    chain = eval(response)[0]['chain']

                    if length > max_length and self.valid_chain(chain):
                        max_length = length
                        new_chain = chain
            except:
                pass

        if (new_chain is not None):
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash, last_proof):
        block_str = (str(last_proof)+str(proof)+previous_hash).encode()
        block_hash = hashlib.sha256(block_str).hexdigest()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sender = '10.188.14.37'
        block = {
            'index': len(self.chain) + 1,
            'sender': sender,
            'timestamp': timestamp,
            'block_hash': block_hash,
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []

        self.chain.append(block)
        with open('blockchain.txt', 'w') as f:
            f.write(str(self.chain))
        return block

    def new_transaction(self, transaction):
        self.current_transactions.append(transaction)

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        last_proof = last_block['proof']
        last_hash = self.hash(last_block)
        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        guess = (str(last_proof)+str(proof)+last_hash).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


def mine(blockchain, node_identifier):
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)
    last_proof = last_block['proof']
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash, last_proof)

    response = [{
        'message': "挖到新的区块",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }]
    return response


def new_transaction(blockchain, transaction):
    trans_id = transaction['trans_id']
    sender = transaction['sender']
    signature = transaction['signature']

    with open('keys.pem', 'r') as f:
        keys = eval(f.read())
    pub = keys[sender]['pub']
    ecc = pyecc.ECC(public=pub)

    if ecc.verify(trans_id, signature):
        index = blockchain.new_transaction(transaction)
        response = [{'message': '签名正确，本事务将被添加到区块: ' + str(index)}]
    else:
        response = [{'message': '签名错误, 拒绝添加'}]
    return response


def full_chain(blockchain):
    response = [{
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }]
    return response


def node_scan(blockchain, ip_whole):
    port = 8000
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(0.2)
    if sk.connect_ex((ip_whole, port)) == 0:
        blockchain.register_node(ip_whole+':'+str(port))
    sk.close()


def register_nodes(blockchain, node_ip):
    if node_ip is None:
        return "Error: Please supply a valid list of nodes", 400

    for i in range(1, 255):
        ip_whole = node_ip+"."+str(i)
        t = Thread(target=node_scan, args=(blockchain, ip_whole))
        t.start()

    total_nodes = ''
    for i in blockchain.nodes:
        total_nodes += i + '\n'

    response = [{
        'message': '发现如下新节点',
        'total_nodes': total_nodes
    }]
    return response


def consensus(blockchain):
    replaced = blockchain.resolve_conflicts()
    if replaced:
        response = [{
            'message': '同步为最长的链',
            'new_chain': blockchain.chain
        }]
    else:
        response = [{
            'message': '没有更长的链',
            'chain': blockchain.chain
        }]
    with open('blockchain.txt', 'w') as f:
        f.write(str(blockchain.chain))

    return response


# delete +1
def get_nodes(blockchain):
    nodes = blockchain.nodes
    response = [{
        'nodes_num': str(len(nodes) + 1)
    }]
    return response


def get_transactions(blockchain):
    transactions = blockchain.current_transactions
    response = [{
        'transactions_num': str(len(transactions))
    }]
    return response


def search_transactions(blockchain, trans_id):
    chain = copy.deepcopy(blockchain.chain)
    chain.reverse()
    for block in chain:
        for transaction in block['transactions']:
            if trans_id == transaction['trans_id']:
                return transaction
                break
    return 'null'


def search_transaction_by_name(blockchain, page_name):
    chain = copy.deepcopy(blockchain.chain)
    chain.reverse()
    for block in chain:
        for transaction in block['transactions']:
            if page_name == transaction['page_name']:
                return transaction
                break
    return 'null'


def page_diff(page_content, last_page_content):
    page_one = page_content.split('\n')
    page_another = last_page_content.split('\n')

    after = ''
    for i in page_one:
        if i not in page_another:
            after += i

    before = ''
    for i in page_another:
        if i not in page_one:
            before += i
    return before, after


global blockchain
blockchain = Blockchain()


@csrf_exempt
def miner(request):
    node_identifier = str(uuid4()).replace('-', '')
    action = request.POST.get('action', None)

    if action == 'mine':
        resp = mine(blockchain, node_identifier)
    elif action == 'new_transaction':
        transaction = request.POST.get('transaction', None)
        resp = new_transaction(blockchain, eval(str(transaction)))
    elif action == 'full_chain':
        resp = full_chain(blockchain)
    elif action == 'register_nodes':
        node_ip = request.POST.get('node_ip', None)
        resp = register_nodes(blockchain, node_ip)
    elif action == 'consensus':
        resp = consensus(blockchain)
    elif action == 'get_nodes':
        resp = get_nodes(blockchain)
    elif action == 'get_transactions':
        resp = get_transactions(blockchain)
    elif action == 'search_transaction_by_name':
        page_name = request.POST.get('page_name', None)
        resp = search_transaction_by_name(blockchain, page_name)
    else:
        resp = [{'message': '请post提交数据'}]

    rjson = json.dumps(resp)
    response = HttpResponse()
    response.write(rjson)
    return response


def block_search(request, block_hash):
    for block in blockchain.chain:
        if block_hash[:64] == block['block_hash']:
            index = block['index']
            sender = block['sender']
            timestamp = block['timestamp']
            trans_list = block['transactions']
            trans_list = copy.deepcopy(trans_list)
            trans_num = len(trans_list)
            for trans in trans_list:
                trans['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S",
                                                   time.localtime(float(
                                                       trans['timestamp'])))
            content = {'index': index, 'sender': sender,
                       'timestamp': timestamp, 'trans_list': trans_list,
                       'trans_num': trans_num}
            return render(request, 'block.html', content)
            break

    trans_id = block_hash[:64]
    transaction_now = search_transactions(blockchain, trans_id)
    if transaction_now == 'null':
        content = {'diff': 'null', 'page_name': 'null'
                   }
    else:
        try:
            trans_id = transaction_now['last_hash']
            page_name = transaction_now['page_name']
            sender = transaction_now['sender']
            timestamp = transaction_now['timestamp']
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S",
                                      time.localtime(float(timestamp)))
            transaction_before = search_transactions(blockchain, trans_id)
            page_content = transaction_now['page_content']
            print '*'*30
            print trans_id
            print transaction_before
            last_page_content = transaction_before['page_content']
            before, after = page_diff(page_content, last_page_content)
            content = {'before': before, 'after': after,
                       'page_name': page_name, 'sender': sender,
                       'timestamp': timestamp
                       }
        except:
            content = {'before': 'null', 'after': page_content,
                       'page_name': page_name, 'sender': sender,
                       'timestamp': timestamp
                       }
    return render(request, 'trans.html', content)
