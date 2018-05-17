#!/usr/bin/env python
# coding=utf-8
from deepdive import *
import sys, re

def is_phrase_list_block(tokens):
	num_tokens = len(tokens)
	i = 0
	while i < num_tokens:
		if (i + 2) < num_tokens and tokens[i] == "sau" and tokens[i + 1] == "đây" and tokens[i + 2] == ":":
			return True
		elif (i + 1) < num_tokens and tokens[i] == "sau" and tokens[i + 1] == ":" :
			return True
		else: i += 1
	return False
## lấy string nếu ngay đằng trước nó là mức phạt
# get_string(tokens, penalty_end_index, 1) in KW1:
def get_string(tokens, start, length):
	if (start + length) < len(tokens):
		return " ".join(word for word in tokens[start + 1: start + length + 1])
#lấy string trong trường hợp luật hình sự#
## lấy string nếu hành vi năm ở giưa câu
def get_crime_string(tokens, key, length):
	num_tokens = len(tokens)
	start = 0
	temp = 0
	for temp in range(0,num_tokens):
		temp_1 = None
		temp_1 = " ".join(word for word in tokens[temp:temp+length])
		if(  temp_1 in key):
			if(temp_1 == "phạt tiền" or temp_1 == "Phạt tiền") :
				if "nếu" in tokens[temp:len(tokens)]:
					return temp
			else:
				return temp
	return 0
def find_character(tokens, start, character):
	i = start + 1
	num_tokens = len(tokens)
	while i < num_tokens:
		if tokens[i] == character: return i
		else: i += 1
@tsv_extractor
@returns(lambda
			mention_id = "text",
			mention_text = "text",
			mention_type = "text",
			law_id = "text",
			position = "text",
			sentence_index = "int",
			begin_index = "int",
			end_index = "int",
			associated_penalty_id = "text"
		 : [])
def extract(
		law_id = "text",
		position = "text",
		sentence_index = "int",
		tokens = "text[]",
		pos_tags = "text[]",
		penalty_id = "text",
		penalty_begin_index = "int",
		penalty_end_index = "int",
		list_sent = "text[]"
):
	# temp = " ".join(word for word in list_sent[0: len(list_sent)])
	# yield [
	# 	None,
	# 	temp,
	# 	None,
	# 	law_id,
	# 	None,
	# 	None,
	# 	None,
	# 	None,
	# 	penalty_id
	# ]
	num_tokens = len(tokens)
	check = 0

	# [PENALTY] ... : a ) ...
	i = penalty_end_index + 1
	phrase_list = None

	# [PENALTY] ... (nếu | đối_với_hành_vi| đối_với trường_hợp | đối_với | trong trường_hợp | đối_với_hành_vi_vi_phạm)
	KW1 = ["hành_vi", "đối_với", "vi_phạm"]
	KW2 = ["đối_với trường_hợp", "trong trường_hợp", "phạt tiền", "Phạt tiền"]
	begin_phrase = None
	end_phrase = None
	if get_string(tokens, penalty_end_index, 2) in KW2:
		begin_phrase = penalty_end_index + 3
	elif get_string(tokens, penalty_end_index, 1) in KW1:
		begin_phrase = penalty_end_index + 2

	elif get_crime_string(tokens, KW2, 2) > 0:
		begin_phrase = get_crime_string(tokens, KW2, 2)
		if begin_phrase > penalty_begin_index :
			begin_phrase = penalty_end_index + 1
	elif get_crime_string(tokens, KW1, 1) > 0:
		begin_phrase = get_crime_string(tokens, KW1, 1)
		if begin_phrase > penalty_begin_index :
			begin_phrase = penalty_end_index + 1

	if begin_phrase :
		if is_phrase_list_block(tokens): check = 1
		if tokens[num_tokens - 1] == ".": end_phrase = num_tokens - 2
		else: end_phrase = num_tokens -1

	if begin_phrase and end_phrase and check == 0:
		begin_index = begin_phrase
		end_index = end_phrase
		# generate a mention identifier
		mention_id = "{}_{}_{}_{}".format(law_id, position, begin_index, end_index)
		mention_text = " ".join(map(lambda k: tokens[k].replace('\\', '\\\\'), range(begin_index, end_index + 1)))
		mention_type = "IN_ONE_SENTENCE"
		associated_penalty_id = penalty_id
		yield [
			mention_id,
			mention_text,
			mention_type,
			law_id,
			position,
			sentence_index,
			begin_index,
			end_index,
			associated_penalty_id
		]
	elif begin_phrase and end_phrase and check == 1 and list_sent is not None:
		begin_index = begin_phrase
		end_index = end_phrase
		# generate a mention identifier
		mention_id = "{}_{}_{}_{}".format(law_id, position, begin_index, end_index)

		mention_text_temp = '\\n'.join(word for word in list_sent[0: len(list_sent)])
		mention_text = " ".join(map(lambda k: tokens[k].replace('\\', '\\\\'), range(begin_index, end_index + 1)))
		mention_text = mention_text + '\\n' + mention_text_temp
		mention_type = "IN_ONE_SENTENCE"
		associated_penalty_id = penalty_id
		yield [
			mention_id,
			mention_text,
			mention_type,
			law_id,
			position,
			sentence_index,
			begin_index,
			end_index,
			associated_penalty_id
		]

