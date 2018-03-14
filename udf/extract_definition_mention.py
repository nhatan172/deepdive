#!/usr/bin/env python
# -*- coding:utf8 -*-


from deepdive import *
import re
import handle_string

def in_bracket(tokens,index) :
	for i in range(0,len(tokens)) :
		if tokens[i] == '(' and i < index:
			for j in range(i+1,len(tokens)) :
				if tokens[j] == ')' :
					if j > index :
						return True
					else :
						break
	return False
def is_candidate(tokens,index) :
	checking_text = " ".join(map(lambda i: tokens[i], xrange(index+1, len(tokens))))
	for i in range(0,index) :
		for j in str.split(tokens[i],"_") :
			if j is not None and j.isalpha() :
				if handle_string.toLowerCase(j) in checking_text:
					return True
	return False
@tsv_extractor
@returns(lambda
	mention_id = "text",
    law_id ="text",
    position ="text",
    sentence_index ="int",
    concept_expression ="text",
    begin_exp = "int",
    end_exp = "int",
    explain_text ="text",
    begin_explain = "int",
    end_explain = "int",
    :[])
def extract(
    law_id  ="text",
    position ="text",
    sentence_index ="int",
    sentence_text ="text",
    tokens ="text[]",
    ):
	
	max_len = len(tokens)
	for i in range(0,max_len) :
		if tokens[i] == 'là' and (not in_bracket(tokens,i)) :
			begin_index = 0
			for j in range(0,i):
				if handle_string.is_upper(tokens[j]) :
					begin_index = j
					break
			end_index = i -1
			if tokens[end_index] == ")":
				while end_index > begin_index:
					if tokens[end_index] == "(" :
						end_index -= 1
						break
					end_index -= 1
			concept_expression = " ".join(map(lambda i: tokens[i], xrange(begin_index, end_index + 1)))
			explain_text = " ".join(map(lambda i: tokens[i], xrange(i+1, len(tokens))))
			mention_id = law_id + "_" +position+ "_"+str(sentence_index) 
			yield [
				mention_id,
				law_id,
				position,
				sentence_index,
				concept_expression,
				begin_index,
				end_index,
				explain_text,
				i+1,
				len(tokens)-1
			]
			break
