#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import divlaw
import handle_string

@tsv_extractor
@returns(lambda
    mention_id   ="text",
    label   ="int",
    rule_id ="text"
    :[])
def extract(
    mention_id ="text",
    sentence_text ="text",
    tokens ="text[]",
    begin_exp ="int",
    end_exp ="int",
    begin_explain ="int",
    end_explain ="int",
    sentence_source ="text[]",
    position_source ="text[]"
    ):
	
	forbidden_word = ["nếu","phải","đó","không","được","đã","đồng_thời","cần", "chỉ",'cụ_thể'] 
	for i in range(2):
		if end_exp +2 +i <= end_explain:
			if handle_string.toLowerCase(tokens[end_exp+2+i]) in forbidden_word:
				yield [
				mention_id,
				-10,
				"forbidden_word_1"
				]
		if end_exp - i >= begin_exp:
			if handle_string.toLowerCase(tokens[end_exp-i]) in forbidden_word:
				yield [
				mention_id,
				-10,
				"forbidden_word_1"
				]
	if handle_string.toLowerCase(tokens[end_exp]) in forbidden_word:
		yield [
		mention_id,
		-1,
		"forbidden_word_2"
		]
	if ("nếu" in tokens[begin_exp:end_exp]) or ("Nếu" in tokens[begin_exp:end_exp]):
		yield [
		mention_id,
		-1,
		"forbidden_word_3"
		]
	i = len(mention_id) - 1
	first = False
	while(i>0) :
		if mention_id[i] == '_' and not first:
			first = True
			i -= 1
			continue
		if mention_id[i] == '_' and first:
			break
		i -= 1
	j = 0
	while(j<len(mention_id)) :
		if mention_id[j] == '_':
			break
		j += 1
	position_require = mention_id[j+1:i+1]
	index = 0
	for index in range(0,len(position_source)):
		if position_require in position_source[index] :
			if divlaw.lenIterator(re.finditer(r"Giải_thích\stừ_ngữ",sentence_source[index],re.U|re.I)) > 0 :
				yield [
					mention_id,
					1,
					"in_explain_words_law"
				]