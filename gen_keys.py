#!/usr/bin/env python
# coding=utf-8

import pyecc


def gen_key(node):
    key = pyecc.ECC.generate()
    keys = {node: {'pub': key._public, 'pri': key._private}}
    with open('keys.pem', 'w') as f:
        f.write(str(keys))


def add_key(node, pub):
    with open('keys.pem', 'r') as f:
        keys = eval(f.read())
    keys[node] = {'pub': pub, 'pri': ''}
    with open('keys.pem', 'w') as f:
        f.write(str(keys))


def test_sign():
    node = '01'
    with open('keys.pem', 'r') as f:
        keys = eval(f.read())
    pub = keys[node]['pub']
    pri = keys[node]['pri']
    ecc = pyecc.ECC(public=pub, private=pri)
    DEFAULT_DATA = '123'
    signature = ecc.sign(DEFAULT_DATA)
    with open('sig', 'w') as f:
        f.write(str(signature))
    print signature


def test_verify():
    node = '01'
    with open('keys.pem', 'r') as f:
        keys = eval(f.read())
    pub = keys[node]['pub']
    ecc = pyecc.ECC(public=pub)
    with open('sig', 'r') as f:
        signature = f.read()
    DEFAULT_DATA = '123'
    print ecc.verify(DEFAULT_DATA, signature)


def main():
    # node = '10.188.14.200'
    # gen_key(node)

    # add other node
    node = '10.188.14.201'
    pub = '!(APD{78n|svng^hC%tAO)YY55Bcv5OKcI)-DnyHH86ae>gq[F*<FK&;.^9~'
    add_key(node, pub)
    # test_sign()
    # test_verify()


if __name__ == '__main__':
    main()
