#-*- coding: utf-8 -*-

import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def print_comment(c):
	print("\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"," \
		"\"%s\",\"%s\",\"%s\""%(c['nickname'], c['userProvince'], \
		c['userLevelName'], c['userClientShow'], c['isMobile'], c['score'], \
		c['creationTime'], c['referenceTime'], c['days'], c['referenceId'], c['content']))

with open('1665416_2017_02_09_11', 'r') as f:
	data = json.load(f)

print("\"nickname\",\"userProvince\",\"userLevelName\",\"userClientShow\"," \
	"\"isMobile\",\"score\",\"creationTime\",\"referenceTime\",\"days\",\"referenceId\",\"content\"")
for i in range(0, len(data)):
	print_comment(data[i])
