#!/usr/bin/env python
# -*- coding:utf8 -*-
from deepdive import *
import sys, re

def check_position(position,sentence_index):
	lenght = len(position)
	if(sentence_index == 1):
		if(int(position[lenght-1]) == 0):
			return 1
		else:
			return 0
	else:
		return 0
def get_range_crime(start,lenght,tokens):
	KW = ["n"]
	for start in range(start,lenght):
		if tokens[start] in KW:
			return start
	return lenght
@tsv_extractor
@returns(lambda
    name_crime = "text",
    info_crime = 'text',
    position = "text",
    law_id = "text",
    sentence_text = "text",
    :[])
def extract(
	law_id = "text",
	position = "text",
	sentence_index = "int",
	sentence_text = "text",
	tokens = "text[]",
):
	num_tokens = len(tokens)
	KW1 = ["tội","Tội"]
	if(check_position(position,sentence_index) == 1):
		for temp in range(0,num_tokens):
			if tokens[temp] in KW1:
				name_crime = " ".join(map(lambda k: tokens[k], range(temp+1, get_range_crime(temp,num_tokens,tokens)-3)))
				if(get_range_crime(temp, num_tokens, tokens) == num_tokens):
					info_crime = None
				else :
					info_crime = " ".join(map(lambda k: tokens[k], range(get_range_crime(temp,num_tokens,tokens)+1,num_tokens-2)))
				yield [
					name_crime,
					info_crime,
					position,
					law_id,
					sentence_text
				]
	
