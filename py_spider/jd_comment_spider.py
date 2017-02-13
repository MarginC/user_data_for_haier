# -*- coding:UTF-8 -*-

import sys
import os
import threading
import urllib.request
import json
import time


def gen_url(productId, page, pageSize=10, score=0):
    domain = 'http://club.jd.com/comment/productPageComments.action'
    params = 'productId={0}&score={1}&sortType=5&page={2}&pageSize={3}'.format(productId, score, page, pageSize)
    _url = domain + '?' + params
    return _url


def get_json(productId, page, pageSize, score):
    _url = gen_url(productId, page, pageSize, score)
    _html = urllib.request.urlopen(_url).read().decode(encoding='gbk', errors='strict')
    _json = json.loads(_html, encoding='gbk')
    return _json


def get_summary(productId):
    _json = get_json(productId, 0, 1, 0)
    return _json['productCommentSummary']


def get_evaluation(score):
    if score > 3:
        return '好评'
    elif score > 1:
        return '中评'
    else:
        return '差评'


def get_comments(productId, page):
    _json = get_json(productId, page, 10, 0)
    return _json['comments']


def write_headers(_file, _headers):
    for header in _headers[:-1]:
        print(header, end=',', file=_file)
    print(_headers[-1], file=_file)


def write_comments(_file, _headers, _comments):
    for comment in _comments:
        comment['evaluation'] = get_evaluation(comment['score'])
        for i in range(len(_headers) - 1):
            print('"{0}"'.format(comment[_headers[i]]), end=',', file=_file)
        print('"{0}"'.format(comment[_headers[-1]]), file=_file)


def write_file(referenceId):
    file_name = referenceId + '.csv'
    if os.path.exists(file_name):
        return
    count = 0
    with open(file_name, mode='w') as file:
        headers = ('nickname', 'userProvince', 'userLevelName', 'userClientShow', 'isMobile', 'score',
                   'evaluation', 'creationTime', 'referenceTime', 'days', 'referenceId', 'content')
        write_headers(file, headers)

        page = 0
        while True:
            try:
                comments = get_comments(referenceId, page)
                if len(comments) > 0:
                    write_comments(file, headers, comments)
                    count += len(comments)
                else:
                    break
            except Exception as e:
                print(e)
            page += 1
    return count


def get_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


class JDThread(threading.Thread):
    def __init__(self, referenceId):
        threading.Thread.__init__(self)
        self.referenceId = referenceId
        self.count = 0

    def run(self):
        self.count = write_file(self.referenceId)

    def get_result(self):
        return self.count


def main():
    referenceIds = sys.argv[1:]
    threads = {}
    print('main process start at {0}'.format(get_time()))
    for referenceId in referenceIds:
        threads[referenceId] = JDThread(referenceId)
        threads[referenceId].start()
        print('{0} start at {1}'.format(referenceId, get_time()))
    while len(referenceIds):
        for referenceId in referenceIds:
            threads[referenceId].join(5)
            if not threads[referenceId].isAlive():
                referenceIds = [i for i in referenceIds if i != referenceId]
                print('{0} crawled {1} comments, stop at {2}'.
                      format(referenceId, threads[referenceId].get_result(), get_time()))
                break;
    print('main process finish at {0}'.format(get_time()))


if __name__ == '__main__':
    main()
