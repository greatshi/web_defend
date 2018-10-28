# coding=utf-8
import hashlib
import random


def compute_hash(message):
    return hashlib.sha256(message).hexdigest()


def generate_nonce():
    return random.randint(1, 1000000000)


def main():
    print compute_hash('123')


if __name__ == '__main__':
    main()
