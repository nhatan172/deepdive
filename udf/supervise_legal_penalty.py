#!/usr/bin/env python
# coding=utf-8
from deepdive import *
import re
from collections import namedtuple
from util.processer import *
import os, sys
import divlaw
import handle_string

LegalPenaltyLabel = namedtuple('LegalPenaltyLabel', 'p_id, label, type')


@tsv_extractor
@returns(lambda
				 mention_id="text",
				 label="int",
				 rule_id="text",
		 : [])
# heuristic rules for finding positive/negative examples of spouse relationship mentions
def supervise(
	mention_id = "text", 
	mention_begin_index = "int", 
	mention_end_index = "int",
	doc_id = "text",
	position =  "text",
	sentence_index = "int",
	sentence_text  = "text",
	tokens = "text[]",
	pos_tags = "text[]"
):
	# # Read keywords from file
	APP_HOME = os.environ['APP_HOME']
	kw_non_legal_penalty = map(lambda word: word.strip(), open(APP_HOME + "/udf/dicts/kw_non_legal_penalty.txt", 'r').readlines())
	kw_legal_penalty = map(lambda word: word.strip(), open(APP_HOME + "/udf/dicts/kw_legal_penalty.txt", 'r').readlines())

	# Non penalty signals on the left of candidate mention
	NON_PENAL_SIGNALS_LEFT = frozenset(kw_non_legal_penalty)
	# Penalty signals on the left of candidate mention
	PENAL_SIGNALS_LEFT = frozenset(kw_legal_penalty)
	# Non capital punishment penalty signals on the left
	NON_CAPITAL_PUNISHMENT = frozenset(["thi_hành án"])

	WINDOW_SIZE = 10
	MAX_PHRASE_LENGTH = 5
	num_tokens = len(tokens)

	# Get all subsequences of left sentence with WINDOW_SIZE = 10
	low_tokens = map(lambda token: token.lower(), tokens)
	left_window = get_left_window(mention_begin_index, low_tokens, WINDOW_SIZE)
	# right_window = get_right_window(p_end, low_tokens, WINDOW_SIZE)
	phrases_in_sentence_left = list(get_all_phrases_in_sentence(left_window, MAX_PHRASE_LENGTH))

	# Get candiate mention text
	candiate_text = " ".join(low_tokens[mention_begin_index:mention_end_index + 1])

	# Get list phrase that contains candidate mention (Example: c ) Phạt tiền từ 30.000.000 đồng đến 50.000.000 đồng trong trường_hợp chậm quá 06 tháng đối_với hạng_mục công_trình , công_trình xây_dựng thuộc dự_án nhóm C ; )
	list_phrase_start, list_phrase_end = get_list_phrase_contains_mention(mention_begin_index, mention_end_index, tokens)
	subphrases_in_list_phrase_left = get_all_phrases_in_sentence(tokens[list_phrase_start: mention_begin_index], 10)

	# regexs
	# (example: 100.000 đồng)
	REGEX_MONEY = ur'^(?:\d+(?:[\.\s]\d{3})*|(?:[^\W\d]|\s)+)(?:\s+triệu)?\s+đồng$'
	# (example: 100.000 đồng đến 200.000 đồng)
	REGEX_MONEY_RANGE = ur'^(?:\d+(?:[\.\s]\d{3})+|(?:[^\W\d]|\s)+)(?:\s+triệu)?\s+đồng(?:[^\W\d]|\s)+(?:\d+(?:[\.\s]\d{3})+|(?:[^\W\d]|\s)+)(?:\s+triệu)?\s+đồng$'
	regex_money = re.compile(REGEX_MONEY, re.UNICODE)
	regex_money_range = re.compile(REGEX_MONEY_RANGE, re.UNICODE)


	# legal_penalty = LegalPenaltyLabel(mention_id = mention_id, label=None, type=None)

	# Negative rules
	# Rule 1: On the left of mention, contains some keywords that appears in kw_non_legal_penalty
	if len(NON_PENAL_SIGNALS_LEFT.intersection(phrases_in_sentence_left)) > 0:
		yield [
			mention_id,
			-1, 
			"neg:non_penalty_signals_left"
		]

	# Rule 2: The first 2 words on the left of mention is "thi_hành án"
	if mention_begin_index >= 2 and tokens[mention_begin_index -1] == 'án' and tokens[mention_begin_index - 2] == 'thi_hành':
		yield[
			mention_id,
			-1,
			"neg:appear_left_thi_hanh_an"
		]

	# Rule 3: The first character on the left or right is a slash (/)
	if (mention_begin_index >=1 and tokens[mention_begin_index -1] == '/') or (mention_begin_index + 1 < num_tokens and tokens[mention_begin_index + 1] == '/'):
		yield [
			mention_id,
			-1, 
			"neg:appear_slash"
		]

	# Rule 4: non capital punishment signals appear on the left mention
	if candiate_text == 'tử_hình' and len(NON_CAPITAL_PUNISHMENT.intersection(phrases_in_sentence_left)) > 0:
		yield [
			mention_id,
			-1,
			"neg:non_capital_punishment_signals"
		]

	# # Rule 5: Sentence contains: "có quyền :" (Example: Trưởng Công_an cấp huyện có quyền : a ) Phạt cảnh_cáo ; b ) Phạt tiền đến 10.000.000 đồng ;)
	# for i in range(p_begin):
	#     if (i + 2) < num_tokens and tokens[i + 1] == "có" and tokens[i + 2] == "quyền":
	#         yield legal_penalty._replace(label=-1, type="neg:sentence_start_with_co_quen")
	#         break

	# # Rule 6: list phrase contains candidate mention is too short (Example: Phạt tiền đến 10.000)
	# if list_phrase_end - list_phrase_start + 1 < 10:
	#     yield legal_penalty._replace(label=-1, type="neg:list_phrase_too_short")

	# Rule 7: In list phrase containing candidate mention, on the left of candidate appears other candidate mentions
	for phrase in subphrases_in_list_phrase_left:
		if regex_money_range.search(phrase.decode('utf8')) or regex_money.search(phrase.decode('utf8')):
			yield [
				mention_id,
				-1,
				"neg:appear_other_mention_left"
			]
			break

	# Rule 8: The sentence that contains mention is in is too short
	if num_tokens < 10:
		yield [
			mention_id,
			-1,
			"neg:sentence_too_short"
		]

	# Positive rules
	# Ruile 1: on the left of mention, containing some keywords that appears in kw_legal_penalty :
	if len(PENAL_SIGNALS_LEFT.intersection(phrases_in_sentence_left)) > 0:
		yield [
			mention_id,
			1, 
			"pos:penalty_signals_left"
		]

	# Rule 2: Candidate mention that match with tù chung_thân, tử_hình
	if candiate_text == 'tù chung_thân' and ('phạt tù' in phrases_in_sentence_left):
		yield [
			mention_id,
			1,
			"pos:life_imprisonment"
		]
	if candiate_text == 'tử_hình' and ('phạt tù' in phrases_in_sentence_left):
		yield [
			mention_id,
			1,
			"pos:capital_punishment"
		]

	# Rules 3: First 2 words on the left mention is "phat tien"
	if mention_begin_index >= 2 and tokens[mention_begin_index - 1].lower() == "phạt" and tokens[mention_begin_index - 2].lower() == "tiền":
		yield [
			mention_id,
			1,
			"pos:before_phat_tien"
		]
