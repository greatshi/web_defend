# coding=utf-8
import os
import time
import stpm


def page_test(page_content):
    if not os.path.exists("page_hash"):
        with open('page_hash', 'w') as f:
            print stpm.compute_hash(page_content)
            f.write(stpm.compute_hash(page_content))
            print 'first'
    with open('page_hash', 'r') as f:
        page_hash = f.read()

    if page_hash == stpm.compute_hash(page_content):
        return True
    else:
        return False


def compute_hash(message):
    return stpm.compute_hash(message)


def generate_nonce():
    return stpm.generate_nonce


def create_time_strap():
    return time.time()


def time_convert(time_strap):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_strap))


def main():
    print page_test('hahaha')
    print time_convert(create_time_strap())
    print page_test('hahaha')
    print page_test('hahahah')


if __name__ == "__main__":
    main()
