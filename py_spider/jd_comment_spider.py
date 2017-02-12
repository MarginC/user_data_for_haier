# -*- coding:UTF-8 -*-

import re
import urllib.request
import json


# isbn = '7513300712'
# url = 'http://openisbn.com/isbn/{0}/'.format(isbn)
# category_pattern = re.compile(r'Category: *.*, ')
# html = urllib.request.urlopen(url).read()
# category_info = category_pattern.findall(html.decode(encoding='utf-8'))
#
# if len(category_info) > 0:
#     print(category_info[0])
# else:
#     print('get category failed.')


def gen_url(productId, page, pageSize=10, score=0):
    domain = 'http://club.jd.com/comment/productPageComments.action'
    params = 'productId={0}&score={1}&sortType=5&page={2}&pageSize={3}'.format(productId, score, page, pageSize)
    _url = domain + "?" + params
    return _url


def get_json(productId, page, pageSize, score):
    _url = gen_url(productId, page, pageSize, score)
    _html = urllib.request.urlopen(_url).read().decode(encoding='gb2312')
    _json = json.loads(_html)
    return _json


def get_summary(productId):
    _json = get_json(productId, 0, 1, 0)
    return _json['productCommentSummary']


def get_comments(productId, page):
    _json = get_json(productId, page, 10, 0)
    return _json['comments']


comments = get_comments(1773994, 0)

print("nickname,userProvince,userLevelName,userClientShow,isMobile")
for i in range(0, len(comments)):
    comment = comments[i]
    print('{0},{1},{2},{3},{4}'
          .format(comment['nickname'], comment['userProvince'], comment['userLevelName']
                  , comment['userClientShow'], comment['isMobile']))
