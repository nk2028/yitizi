# -*- coding: utf-8 -*-

import json
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'yitizi.json'), encoding='utf8') as f:
	yitizi_data = json.load(f)

def get(c):
	'''
	Input a Chinese character. Output all the variant characters of it.

	```
	>>> import yitizi
	>>> yitizi.get('和')
	['咊', '龢']
	```
	'''

	assert len(c) == 1, 'Expected a single character'

	res = yitizi_data.get(c)
	if res:
		return list(res)
	else:
		return []  # return empty list if the given character has no variant characters
