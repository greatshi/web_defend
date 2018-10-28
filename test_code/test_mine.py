# coding=utf-8
import hashlib
import time


def test_mine(last_proof, last_hash):
    proof = 0
    while True:
        hash = hashlib.sha256(str(last_proof) +
                              str(proof) + last_hash).hexdigest()
        print hash
        if hash[:5] == "00000":
            break
        proof += 1
    return str(proof), hash


def main():
    print(time.time())
    print(test_mine(3799,
          '0000064be2423ebb5f58b7c861e5452525b908e3e0cf9a6a221f38f34ef071b3'))
    print(time.time())


if __name__ == '__main__':
    main()
